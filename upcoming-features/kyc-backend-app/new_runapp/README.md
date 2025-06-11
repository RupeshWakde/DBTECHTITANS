# KYC API Application Runner

This folder contains comprehensive scripts and tools to run the KYC FastAPI application with proper configuration, environment setup, and error handling.

## Features

- 🚀 **Easy Application Startup**: Multiple ways to start the KYC API application
- 🔧 **Environment Configuration**: Automatic environment setup (AWS/Local)
- 📦 **Dependency Checking**: Verifies all required packages are installed
- 🗄️ **Database Initialization**: Automatically initializes the database connection
- ☁️ **Storage Testing**: Tests S3 storage connection
- 🏥 **Health Checks**: Optional health check functionality
- 🛑 **Graceful Shutdown**: Handles shutdown signals properly
- 🐛 **Development Mode**: Auto-reload for development
- 📊 **Logging**: Comprehensive logging and status messages
- ⚙️ **Configuration Management**: JSON-based configuration system

## Files Overview

| File | Description | Platform |
|------|-------------|----------|
| `run_app.py` | Main Python application runner | All |
| `launcher.py` | Configuration-based launcher | All |
| `run_app.sh` | Shell script for Linux/macOS | Linux/macOS |
| `run_app.bat` | Batch file for Windows | Windows |
| `run_app.ps1` | PowerShell script for Windows | Windows |
| `config.json` | Configuration file | All |
| `README.md` | This documentation | All |

## Quick Start

### Method 1: Direct Python Script

```bash
# Run from the new_runapp directory
python run_app.py
```

### Method 2: Configuration-Based Launcher

```bash
# Development mode
python launcher.py dev

# Production mode
python launcher.py production

# Testing mode
python launcher.py test
```

### Method 3: Platform-Specific Scripts

**Windows (Command Prompt):**
```cmd
run_app.bat
```

**Windows (PowerShell):**
```powershell
.\run_app.ps1
```

**Linux/macOS:**
```bash
./run_app.sh
```

## Configuration

The `config.json` file contains predefined environments and settings:

### Environments

- **Development**: Local development with auto-reload and debugging
- **Production**: Production deployment with multiple workers
- **Testing**: Testing environment with health checks

### Customizing Configuration

Edit `config.json` to modify default settings:

```json
{
    "environments": {
        "development": {
            "host": "127.0.0.1",
            "port": 8080,
            "workers": 1,
            "dev_mode": true,
            "health_check": true
        }
    }
}
```

## Command Line Options

### Main Runner (`run_app.py`)

| Option | Description | Default |
|--------|-------------|---------|
| `--host` | Host to bind to | `0.0.0.0` |
| `--port` | Port to bind to | `8000` |
| `--dev`, `-d` | Enable development mode with auto-reload | `False` |
| `--workers` | Number of worker processes | `1` |
| `--subprocess` | Use subprocess to run the application | `False` |
| `--health-check` | Run health check after startup | `False` |

### Launcher (`launcher.py`)

| Command | Description |
|---------|-------------|
| `python launcher.py dev` | Run in development mode |
| `python launcher.py production` | Run in production mode |
| `python launcher.py test` | Run in testing mode |
| `python launcher.py --config` | Show current configuration |
| `python launcher.py --help` | Show help information |

### Shell Script (`run_app.sh`)

| Option | Description |
|--------|-------------|
| `--host HOST` | Host to bind to |
| `--port PORT` | Port to bind to |
| `--dev`, `-d` | Enable development mode |
| `--workers NUM` | Number of worker processes |
| `--health-check` | Run health check |
| `--help`, `-h` | Show help message |

## Usage Examples

### Development Workflow

```bash
# Using launcher (recommended)
python launcher.py dev

# Using direct script
python run_app.py --dev --host 127.0.0.1 --port 8080

# Using shell script
./run_app.sh --dev --port 8080
```

### Production Deployment

```bash
# Using launcher
python launcher.py production

# Using direct script
python run_app.py --host 0.0.0.0 --port 8000 --workers 4

# Using shell script
./run_app.sh --host 0.0.0.0 --port 8000 --workers 4
```

### Testing

```bash
# Using launcher
python launcher.py test

# Using direct script
python run_app.py --dev --health-check

# Using shell script
./run_app.sh --dev --health-check
```

## Environment Configuration

The scripts automatically configure the environment:

- **AWS Mode** (default): Sets `ENV=aws` for production deployment
- **Local Mode**: Sets `ENV=local` when `--dev` flag is used

## Dependencies

The scripts check for the following required packages:
- `fastapi`
- `uvicorn`
- `sqlalchemy`
- `psycopg2-binary`
- `pydantic`
- `boto3`

If any dependencies are missing, the scripts will provide instructions to install them.

## Error Handling

All scripts include comprehensive error handling:

- **Import Errors**: Checks for missing application modules
- **Database Errors**: Handles database connection failures gracefully
- **Storage Errors**: Continues running even if S3 connection fails
- **Health Check Errors**: Non-blocking health check failures
- **Configuration Errors**: Validates configuration files

## Logging

All scripts provide detailed logging with emojis for easy identification:

- 🔧 Setup operations
- 📦 Dependency checks
- 🗄️ Database operations
- ☁️ Storage operations
- 🚀 Application startup
- 🏥 Health checks
- 🛑 Shutdown operations
- ✅ Success messages
- ❌ Error messages
- ⚠️ Warning messages

## File Structure

```
new_runapp/
├── run_app.py          # Main application runner script
├── launcher.py         # Configuration-based launcher
├── run_app.sh          # Shell script for Linux/macOS
├── run_app.bat         # Batch file for Windows
├── run_app.ps1         # PowerShell script for Windows
├── config.json         # Configuration file
└── README.md          # This documentation file
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure you're running the script from the correct directory
2. **Database Connection**: Check your database configuration in `config.py`
3. **Port Already in Use**: Use a different port with `--port` option
4. **Missing Dependencies**: Run `pip install -r requirements.txt`
5. **Permission Errors**: Make shell scripts executable with `chmod +x run_app.sh`

### PostgreSQL Driver Issues (Windows)

The most common issue on Windows is with the PostgreSQL driver (`psycopg2-binary`). The scripts now handle this automatically, but if you encounter issues:

#### Automatic Fix
```bash
# Use the installer script
python new_runapp/install_postgres.py

# Or use the batch file with dependency installation
run_app.bat --install-deps
```

#### Manual Solutions
1. **Try alternative drivers**:
   ```bash
   pip install psycopg2
   # or
   pip install psycopg
   ```

2. **Install Visual Studio Build Tools**:
   - Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
   - Install C++ build tools
   - Then run: `pip install psycopg2`

3. **Use conda** (if available):
   ```bash
   conda install psycopg2
   ```

4. **Download pre-compiled wheel**:
   - Visit: https://www.lfd.uci.edu/~gohlke/pythonlibs/#psycopg
   - Download appropriate wheel for your Python version
   - Install with: `pip install <wheel_file>`

#### Alternative Drivers
- `psycopg2`: Standard PostgreSQL driver
- `psycopg`: Newer PostgreSQL driver
- `asyncpg`: Async PostgreSQL driver

### Debug Mode

For debugging, use development mode:
```bash
python launcher.py dev
# or
python run_app.py --dev --health-check
```

This will:
- Enable auto-reload
- Run health checks
- Provide detailed logging

## Integration

The scripts are designed to work seamlessly with:
- Docker containers
- CI/CD pipelines
- Production deployment scripts
- Development workflows
- Cloud platforms (AWS, Azure, GCP)

## Security Notes

- The scripts run on `0.0.0.0` by default for production
- Use `127.0.0.1` for local development
- Ensure proper firewall configuration in production
- Use environment variables for sensitive configuration
- Review security settings in `config.json`

## Platform-Specific Notes

### Windows
- Use `run_app.bat` for Command Prompt
- Use `run_app.ps1` for PowerShell
- Ensure Python is in your PATH

### Linux/macOS
- Use `run_app.sh` for shell access
- Make script executable: `chmod +x run_app.sh`
- Python 3 is recommended

### Cross-Platform
- `run_app.py` and `launcher.py` work on all platforms
- Use `launcher.py` for configuration-based deployment

## Support

For issues or questions:
1. Check the error messages in the console output
2. Verify all dependencies are installed
3. Check the application logs
4. Review the configuration files
5. Try running with `--help` for usage information 