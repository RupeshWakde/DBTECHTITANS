# KYC Python App - AWS Version

A FastAPI-based KYC (Know Your Customer) application configured to use AWS PostgreSQL (RDS) and S3 storage. This is a standalone version of the original KYC API, optimized for AWS cloud deployment.

## 🚀 Features

- **Complete KYC Workflow**: User registration, document upload, details submission, and progress tracking
- **AWS PostgreSQL Integration**: Uses RDS PostgreSQL for data persistence
- **S3 File Storage**: Secure document storage in AWS S3
- **Mock Document Extraction**: Simulated OCR for Aadhaar, PAN, and Passport documents
- **Health Monitoring**: Built-in health checks for database and S3 connectivity
- **CORS Support**: Cross-origin resource sharing enabled
- **Comprehensive API**: Full REST API with documentation

## 📋 Prerequisites

- Python 3.8 or higher
- AWS account with:
  - PostgreSQL RDS instance
  - S3 bucket for file storage
  - AWS credentials configured
- Access to AWS Secrets Manager (for database credentials)

## 🛠️ Installation

1. **Clone and navigate to the project:**
   ```bash
   cd kyc-api-app/kyc-python-app
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   # AWS Configuration
   export AWS_ACCESS_KEY_ID=your_access_key
   export AWS_SECRET_ACCESS_KEY=your_secret_key
   export AWS_SESSION_TOKEN=your_session_token  # For temporary credentials
   export AWS_REGION=us-east-2
   
   # Environment
   export ENV=aws
   ```

## 🏃‍♂️ Running the Application

### Local Development
```bash
python run_local.py
```

The API will be available at:
- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 📚 API Endpoints

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | API information and available endpoints |
| `GET` | `/health` | Health check with AWS service status |
| `POST` | `/register` | Register a new user |
| `GET` | `/kyc/case` | Create a new KYC case |
| `POST` | `/kyc/upload` | Upload KYC documents to S3 |
| `POST` | `/kyc/details` | Submit KYC details |
| `GET` | `/kyc/screen-data/{case_id}` | Get KYC screen data |
| `GET` | `/kyc/progress/{case_id}` | Get KYC progress |
| `GET` | `/customers` | List all customers |

### Request Examples

#### User Registration
```bash
curl -X POST "http://localhost:8000/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "phone": "+1234567890",
    "password": "securepassword",
    "emailVerified": true,
    "phoneVerified": true,
    "securityQuestions": ["What is your mother's maiden name?"],
    "kyc_case_id": 1
  }'
```

#### KYC Details Submission
```bash
curl -X POST "http://localhost:8000/kyc/details" \
  -H "Content-Type: application/json" \
  -d '{
    "kyc_case_id": 1,
    "name": "John Doe",
    "dob": "1990-01-01",
    "gender": "Male",
    "address": "123 Main St, City",
    "father_name": "Father Name",
    "pan_number": "ABCDE1234F",
    "aadhar_number": "123456789012",
    "email": "user@example.com",
    "phone": "+1234567890",
    "occupation": "Software Engineer",
    "source_of_funds": "Salary",
    "business_type": "Individual",
    "is_pep": false,
    "annual_income": "500000",
    "purpose_of_account": "Personal",
    "nationality": "Indian",
    "marital_status": "Single"
  }'
```

#### Document Upload
```bash
curl -X POST "http://localhost:8000/kyc/upload" \
  -F "kyc_case_id=1" \
  -F "doc_type=aadhar_front" \
  -F "file=@/path/to/aadhar_front.jpg"
```

## 🧪 Testing

### Run API Tests
```bash
python test_api.py
```

### Test Specific Endpoint
```bash
python test_api.py http://localhost:8000
```

## 📁 Project Structure

```
kyc-python-app/
├── main.py                 # Main FastAPI application
├── requirements.txt        # Python dependencies
├── run_local.py           # Local development runner
├── test_api.py            # API testing script
└── README.md              # This file
```

## 🔧 Configuration

### Database Configuration
The application uses the parent directory's database configuration:
- **File**: `../database.py`
- **Environment**: AWS PostgreSQL (RDS)
- **Credentials**: Retrieved from AWS Secrets Manager

### Storage Configuration
- **File**: `../storage.py`
- **Service**: AWS S3
- **Bucket**: Configured in AWS environment

### Models
- **File**: `../models.py`
- **ORM**: SQLAlchemy
- **Tables**: User, KycCase, KycDocument, KycDetail, KycStatus

## 🔒 Security Features

- **Password Hashing**: Secure password storage (implement in production)
- **Input Validation**: Pydantic models for request validation
- **CORS Configuration**: Configurable cross-origin settings
- **Database Connection Pooling**: Efficient database connections
- **Error Handling**: Comprehensive error handling and logging

## 🚨 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Check AWS credentials
   - Verify RDS security groups
   - Ensure Secrets Manager access

2. **S3 Upload Error**
   - Check S3 bucket permissions
   - Verify AWS credentials
   - Check bucket name configuration

3. **Import Errors**
   - Ensure all dependencies are installed
   - Check Python path configuration
   - Verify parent directory imports

### Debug Mode
Enable debug logging by setting environment variable:
```bash
export LOG_LEVEL=DEBUG
```

## 📊 Health Check Response

```json
{
  "status": "healthy",
  "environment": "aws",
  "timestamp": "2024-01-01T00:00:00",
  "database": "connected",
  "s3": "connected"
}
```

## 🔄 KYC Workflow

1. **Create KYC Case** → Get case ID
2. **Register User** → Create user account
3. **Upload Documents** → Upload to S3
4. **Submit Details** → Save KYC information
5. **Track Progress** → Monitor completion status

## 📈 Monitoring

- **Health Endpoint**: Monitor database and S3 connectivity
- **Logs**: Check application logs for errors
- **AWS CloudWatch**: Monitor RDS and S3 metrics
- **API Documentation**: Interactive docs at `/docs`

## 🤝 Support

For issues and questions:
1. Check the health endpoint for system status
2. Review application logs
3. Verify AWS service connectivity
4. Test endpoints individually

## 📝 License

This project is part of the KYC API application suite. 