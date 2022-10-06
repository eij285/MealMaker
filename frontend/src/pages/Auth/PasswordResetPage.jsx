import React from 'react';
import AuthLayout from '../../components/Layout/AuthLayout';

function PasswordResetPage () {
  const query = new URLSearchParams(window.location.search);
  const email = query.get("email");
  const resetCode = query.get("code");
  console.log(email, resetCode);
  return (
    <AuthLayout>
      PasswordResetPage
    </AuthLayout>
  );
}

export default PasswordResetPage;
