import asyncio as _asyncio


async def run_shell_cmd(cmd: str) -> (int, str, str):
    """Execute shell command

    Returns:
      Tuple (returned code, stdout, stderr)
    """
    proc = await _asyncio.create_subprocess_shell(
        cmd, stdout=_asyncio.subprocess.PIPE, stderr=_asyncio.subprocess.PIPE)
    stdout, stderr = await proc.communicate()
    return proc.returncode, stdout.decode().strip(), stderr.decode().strip()
