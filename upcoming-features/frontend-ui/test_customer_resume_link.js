// Test script to verify customer resume link mapping
// This script can be run in the browser console on the customers page

async function testCustomerResumeLinks() {
  console.log('🧪 Testing Customer Resume Link Mapping');
  console.log('=' .repeat(60));
  
  try {
    // Step 1: Get customers data from the API
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    const response = await fetch(`${apiUrl}/customers`);
    
    if (!response.ok) {
      throw new Error('Failed to fetch customers');
    }
    
    const customers = await response.json();
    console.log('📋 API Response:', customers);
    
    // Step 2: Check if kyc_case_id is present in the response
    customers.forEach((customer, index) => {
      console.log(`\n👤 Customer ${index + 1}:`);
      console.log(`   Name: ${customer.name}`);
      console.log(`   Email: ${customer.email}`);
      console.log(`   KYC Details ID: ${customer.kyc_details_id}`);
      console.log(`   KYC Case ID: ${customer.kyc_case_id}`);
      console.log(`   Status: ${customer.status}`);
      
      // Verify the mapping
      if (customer.kyc_case_id) {
        console.log(`   ✅ KYC Case ID present: ${customer.kyc_case_id}`);
        console.log(`   🔗 Resume link should be: /self-kyc/${customer.kyc_case_id}`);
      } else {
        console.log(`   ❌ KYC Case ID missing!`);
      }
    });
    
    // Step 3: Check if the frontend is using the correct data
    console.log('\n🔍 Checking frontend data transformation...');
    
    // Simulate the frontend transformation
    const transformedCustomers = customers.map(customer => ({
      id: customer.kyc_details_id.toString(),
      kycCaseId: customer.kyc_case_id.toString(),
      name: customer.name || 'N/A',
      email: customer.email || 'N/A'
    }));
    
    console.log('📊 Transformed Customers:', transformedCustomers);
    
    // Step 4: Verify resume links
    console.log('\n🔗 Resume Link Verification:');
    transformedCustomers.forEach((customer, index) => {
      const resumeLink = `/self-kyc/${customer.kycCaseId}`;
      console.log(`   Customer ${index + 1}: ${customer.name}`);
      console.log(`   Resume Link: ${resumeLink}`);
      console.log(`   KYC Case ID used: ${customer.kycCaseId}`);
      
      // Test if the link would work
      if (customer.kycCaseId && customer.kycCaseId !== 'undefined') {
        console.log(`   ✅ Valid resume link`);
      } else {
        console.log(`   ❌ Invalid resume link - missing kycCaseId`);
      }
    });
    
    console.log('\n🎉 Test completed successfully!');
    
  } catch (error) {
    console.error('❌ Test failed:', error);
  }
}

// Instructions for running this test:
console.log(`
📝 Instructions:
1. Open the customers page in your browser
2. Open browser developer tools (F12)
3. Go to the Console tab
4. Copy and paste this entire script
5. Press Enter to run the test
6. Check the console output for verification results
`);

// Export the function for manual testing
window.testCustomerResumeLinks = testCustomerResumeLinks; 