#!/bin/bash

echo "🌐 Testing CORS headers from nginx server..."
echo "🔗 URL: http://ec2-13-59-44-211.us-east-2.compute.amazonaws.com:8000"

echo ""
echo "🧪 Test 1: Simple GET request"
curl -I -H "Origin: https://main.d9aah2ia177kc.amplifyapp.com" \
     GET http://ec2-13-59-44-211.us-east-2.compute.amazonaws.com:8000/cors-test

echo ""
echo "🧪 Test 2: OPTIONS preflight request"
curl -I -X OPTIONS \
     -H "Origin: https://main.d9aah2ia177kc.amplifyapp.com" \
     -H "Access-Control-Request-Method: GET" \
     -H "Access-Control-Request-Headers: Content-Type" \
     GET http://ec2-13-59-44-211.us-east-2.compute.amazonaws.com:8000/customers

echo ""
echo "🧪 Test 3: GET request to customers endpoint"
curl -I -H "Origin: https://main.d9aah2ia177kc.amplifyapp.com" \
     GET http://ec2-13-59-44-211.us-east-2.compute.amazonaws.com:8000/customers

echo ""
echo "✅ CORS test complete!" 