module.exports = {
    apps: [
        {
            name: 'DL Gaceta',
            script: '/home/fastapiuser/gacetachat/venv/bin/python',
            args: '/home/fastapiuser/gacetachat/download_gaceta.py',
            interpreter: '/home/fastapiuser/gacetachat/venv/bin/python', // path to the Python interpreter
            exec_mode: 'fork',
            watch: true,
            env: {
                NODE_ENV: 'development',
                // Custom environment variables for this instance
            },
        },
        {
            name: 'FastAPIApp',
            script: '/home/fastapiuser/gacetachat/venv/bin/uvicorn',
            args: 'fastapp:app --host 127.0.0.1 --port 8050', // Specify the main file and the app object
            interpreter: '/home/fastapiuser/gacetachat/venv/bin/python', // path to the Python interpreter
            exec_mode: 'fork',
            watch: true,
            env: {
                NODE_ENV: 'development',
                // Custom environment variables for this instance
            }
        },
        {
            name: 'StreamlitApp',
            script: '/home/fastapiuser/gacetachat/venv/bin/streamlit',
            args: 'run /home/fastapiuser/gacetachat/app.py --server.port 8512', // Specify the main file to run
            interpreter: '/home/fastapiuser/gacetachat/venv/bin/python', // path to the Python interpreter
            exec_mode: 'fork',
            watch: true,
            env: {
                NODE_ENV: 'development',
                // Custom environment variables for this instance
            }
        }
        // Add more instances as needed
    ]
};