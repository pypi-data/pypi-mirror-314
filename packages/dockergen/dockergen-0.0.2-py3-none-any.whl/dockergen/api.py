
from dataclasses import dataclass
import json

from typing import IO, Any, Dict, List, Optional, Union

def _quote(s: str):
    '''Return original string 's' as-is if it's something that doesn't
    need to be enclosed in string literals in a Dockerfile.
    Otherwise add quotes.

    Examples:
        "Firstname Lastname <email@example.org>"
        -> use quotes

        mypage:v1.0
        -> no need for quotes
    '''
    # TODO review what type of quoting is really required
    if ' ' in s:
        return f'"{s}"'
    return s

def shellify(cmds: List[str]):
    cstrs = []
    for c in cmds:
        cs = [c.lstrip() for c in c.split('\n')]
        cstrs.append(' \\\n    '.join(cs))
    cstr = ' \\\n && '.join(cstrs)
    return cstr

class BaseInstruction:
    def output(self, fp: IO[str]):
        raise NotImplemented

@dataclass
class From(BaseInstruction):
    image_tag: str
    platform: Optional[str]
    as_: Optional[str]
    def write(self, fp: IO[str]):
        parts = ['FROM']
        if self.platform is not None:
            parts.append(f'--platform={self.platform}')
        parts.append(self.image_tag)
        if self.as_ is not None:
            parts.append(f'AS {self.as_}')
        fp.write(' '.join(parts) + '\n')

@dataclass
class Label(BaseInstruction):
    metadata_kv: Dict[str, Any]
    def write(self, fp: IO[str]):
        kvs = [f'{k}={_quote(v)}' for k,v in self.metadata_kv.items()]
        fp.write(f'LABEL {" ".join(kvs)}\n')

@dataclass
class Env(BaseInstruction):
    env_kv: Dict[str, Any]
    def write(self, fp: IO[str]):
        kvs = [f'{k}={_quote(v)}' for k,v in self.env_kv.items()]
        fp.write(f'ENV {" ".join(kvs)}\n')

@dataclass
class Mount:
    from_: Optional[str]
    source: Optional[str]
    target: Optional[str]
    type_: str = 'bind'

    def to_string(self) -> str:
        assert self.type_ == 'bind' # only bind supported for now
        return f'--mount=type={self.type_},from={self.from_},source={self.source},target={self.target}'

@dataclass
class Run(BaseInstruction):
    commands: Union[str, List[str]]
    mount: Union[List[Mount], Optional[Mount]]
    def write(self, fp: IO[str]):
        mount = ''
        if self.mount is not None:
            if isinstance(self.mount, list):
                mount = ' '.join([x.to_string() for x in self.mount])
            else:
                mount = f'{self.mount.to_string()}'
            mount += ' '
        if isinstance(self.commands, list):
            fp.write(f'RUN {mount}{json.dumps(self.commands)}\n')
        else:
            fp.write(f'RUN {mount}{self.commands}\n')

@dataclass
class Copy(BaseInstruction):
    source: Union[str, List[str]]
    dest: str
    chown: Optional[str]
    from_: Optional[str]
    def write(self, fp: IO[str]):
        chown = f'--chown={self.chown} ' if self.chown is not None else ''
        from_ = f'--from={self.from_} ' if self.from_ is not None else ''
        if isinstance(self.source, list):
            fp.write(f'COPY {from_}{chown}{" ".join(_quote(s) for s in self.source)} {_quote(self.dest)}\n')
        else:
            fp.write(f'COPY {from_}{chown}{_quote(self.source)} {_quote(self.dest)}\n')

@dataclass
class Workdir(BaseInstruction):
    workdir: str
    def write(self, fp: IO[str]):
        fp.write(f'WORKDIR {_quote(self.workdir)}\n')

class Gen:
    def __init__(self):
        self._instrs = []

    def from_(self, image_tag: str, platform: Optional[str] = None, as_: Optional[str] = None):
        '''The FROM instruction initializes a new build stage and sets the
        Base Image for subsequent instructions. As such, a valid Dockerfile
        must start with a FROM instruction.

        Args:
            image_tag: Docker base image name and tag
            as_: Stage name for multi-stage builds
        '''
        self._instrs.append(From(image_tag, platform, as_))

    def label(self, **args):
        self._instrs.append(Label(dict(**args)))

    def env(self, **args):
        self._instrs.append(Env(dict(**args)))

    def run(self, commands: Union[List[str], str], mount: Union[List[Mount], Optional[Mount]] = None, shell: bool = True):
        if not shell:
            # RUN 'exec' form requires a list
            assert isinstance(commands, list)
            self._instrs.append(Run(commands, mount))
        else:
            if isinstance(commands, list):
                self._instrs.append(Run(shellify(commands), mount))
            else:
                assert isinstance(commands, str)
                self._instrs.append(Run(commands, mount))

    def run_exec(self, command: List[str]):
        '''RUN command but use an explicit list to perform an exec invocation without shell'''
        raise NotImplemented

    def copy(self, source: Union[List[str], str], dest: str, chown: Optional[str] = None, from_: Optional[str] = None):
        self._instrs.append(Copy(source, dest, chown, from_))

    def workdir(self, workdir: str):
        self._instrs.append(Workdir(workdir))

    def write(self, fp: IO[str]):
        for instr in self._instrs:
            instr.write(fp)
