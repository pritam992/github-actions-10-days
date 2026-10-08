"""Single-instance teaching deployment; brief downtime, no automatic rollback."""
import json
import os
import re
import shlex
import subprocess
import time
from pathlib import Path


def aws(*args):
    return json.loads(subprocess.check_output(['aws', *args, '--output', 'json'], text=True))


tag = os.environ['IMAGE_TAG']
if not re.fullmatch(r'[0-9a-f]{40}', tag):
    raise SystemExit('image_tag must be a full lowercase 40-character commit SHA')
registry = os.environ['REGISTRY']
repository = os.environ['REPOSITORY']
region = os.environ['AWS_REGION']
image = f'{registry}/{repository}:{tag}'
q = shlex.quote
commands = [
    'set -eu',
    f'aws ecr get-login-password --region {q(region)} > /tmp/bootcamp-ecr-password',
    f'docker login --username AWS --password-stdin {q(registry)} < /tmp/bootcamp-ecr-password',
    'rm -f /tmp/bootcamp-ecr-password',
    f'docker pull {q(image)}',
    'docker rm -f bootcamp 2>/dev/null || true',
    f'docker run -d --name bootcamp --restart unless-stopped -p 127.0.0.1:8080:8000 {q(image)}',
    'ok=0; for n in 1 2 3 4 5 6 7 8 9 10; do if curl -fsS http://127.0.0.1:8080/health; then ok=1; break; fi; sleep 3; done; test "$ok" -eq 1',
]
parameters = Path('ssm-parameters.json')
parameters.write_text(json.dumps({'commands': commands}))
result = aws('ssm', 'send-command', '--instance-ids', os.environ['INSTANCE_ID'],
             '--document-name', 'AWS-RunShellScript', '--parameters', 'file://' + str(parameters))
command_id = result['Command']['CommandId']
print('SSM command:', command_id)
for _ in range(120):
    try:
        result = aws('ssm', 'get-command-invocation', '--command-id', command_id,
                     '--instance-id', os.environ['INSTANCE_ID'])
    except subprocess.CalledProcessError:
        time.sleep(5)
        continue
    status = result['Status']
    if status in ('Pending', 'InProgress', 'Delayed'):
        time.sleep(5)
        continue
    print(result.get('StandardOutputContent', ''))
    print(result.get('StandardErrorContent', ''))
    if status != 'Success':
        raise SystemExit('Deployment failed: ' + status)
    break
else:
    raise SystemExit('Timed out waiting for SSM; inspect the command in AWS before retrying')
