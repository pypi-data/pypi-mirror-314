from string import Template
import os


def read_env_file(file_path):
    env_vars = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    env_vars.append(line.strip())
        return env_vars
    except:
        with open(file_path, 'r', encoding='utf-16') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    env_vars.append(line.strip())
        return env_vars


def get_dockerfile_template(language: str, port: int, version: str, envs: tuple, env_file: str) -> str:
    """
    Returns the Dockerfile template for the specified language and version.

    Args:
        version (str): The version of the programming language.
        port (float): The port on which the container will run.
        envs (tuple): A tuple of environment variables to be included in the Dockerfile. Each element is a string
                      representing a key-value pair (e.g., ("ENV_VAR1=value1"), ("ENV_VAR2=value2")). These environment
                      variables are directly added to the Dockerfile with the 'ENV' instruction.
        env_file (str): Path to a file containing additional environment variables. Each line of the file should
                        contain a key-value pair formatted as `KEY=value`. These variables are read and also included
                        in the Dockerfile as `ENV` instructions.

    Returns:
        str: The Dockerfile template.
    """

    version = version + '-alpine'
    if env_file is not None:
        env_file = "\n".join([f"ENV {var}" for var in read_env_file(env_file)])
    else:
        env_file = ""
    envs = "".join([f'ENV {env}\n' for env in envs])

    if language == 'django' and version == 'lts-alpine':
        version = 'alpine'

    templates = {
        'django': f'''FROM python:{version}
        
    EXPOSE {port}
    
    WORKDIR /app
    
    COPY . /app
    {envs}
    {env_file}
    RUN pip3 install -r requirements.txt
    
    RUN python manage.py collectstatic --noinput
    
    ENTRYPOINT ["python3"]
    CMD ["manage.py", "runserver", "0.0.0.0:{port}"]''',
        'vite': f'''FROM node:{version} AS build
    
    WORKDIR /app
    
    COPY package.json /app
    COPY package-lock.json /app
    RUN npm install
    
    COPY . /app
    RUN npm run build
    
    FROM nginx:alpine
    {envs}
    {env_file}
    COPY --from=build /app/dist /usr/share/nginx/html
    EXPOSE {port}
    CMD ["nginx", "-g", "daemon off;"]
    ''',
        'react': f'''FROM node:{version} AS build

    WORKDIR /app

    COPY package.json /app
    COPY package-lock.json /app
    RUN npm install

    COPY . /app
    RUN npm run build

    FROM nginx:alpine
    {envs}
    {env_file}
    COPY --from=build /app/build /usr/share/nginx/html
    EXPOSE {port}
    CMD ["nginx", "-g", "daemon off;"]
    ''', 'nextjs': f'''

FROM node:{version} AS builder

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm install

COPY . .

{envs}
{env_file}

RUN npm run build

FROM node:{version} AS production

WORKDIR /app

COPY --from=builder /app/package.json ./
COPY --from=builder /app/package-lock.json ./
RUN npm install --production

COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public

{envs}
{env_file}
EXPOSE {port}

CMD ["npm", "start"]
    '''
    }
    return templates.get(language.lower(), "Unsupported language")
