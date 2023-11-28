<template>
  <div>
    <h2>Register</h2>
    <form @submit.prevent="handleSignUp">
      <label for="username">Username: </label>
      <input
        type="text"
        id="username"
        ref="usernameInput"
        v-model="username"
        placeholder="Enter your username"
        required
      />
      <br />
      <label for="password">Password: </label>
      <input
        type="password"
        id="password"
        ref="passwordInput"
        v-model="password"
        placeholder="Enter your password"
        required
      />
      <br />
      <br />
      <label for="email">Email: </label>
      <input
        type="email"
        id="email"
        ref="emailInput"
        v-model="email"
        placeholder="Enter your email id"
        required
      />
      <br />
      <br />
      <button type="submit">Sign Up</button>
    </form>
    <p v-if="err" style="color: red">{{ errorMessage }}</p>
  </div>
</template>

<script setup>
  import { ref } from 'vue';
  import { useRouter } from 'vue-router';

  const router = useRouter();
  // Create refs for username and password input fields
  const usernameInput = ref(null);
  const passwordInput = ref(null);
  const emailInput = ref(null);

  // Data properties
  const username = ref('');
  const password = ref('');
  const email = ref('');

  // const error = ref('');
  const errorMessage = ref('');
  const err= ref(false);
  // Function to handle sign up
// ... (import statements and other setup code) ...

const handleSignUp = () => {
  if (!usernameInput.value.validity.valid || !passwordInput.value.validity.valid || !emailInput.value.validity.valid) {
    return;
  }

  const userData = {
    "username": username.value,
    "password": password.value,
    "email": email.value
  };

  fetch('http://127.0.0.1:5000/api/register', {
    method: 'POST',
    body: JSON.stringify(userData),
    headers: {
      'Content-Type': 'application/json'
    }
  })
  .then(response => {
    if (!response.ok) {
      err.value = true;
      return response.json();
    } else {
      err.value = false;
      return response.json();
    }
  })
  .then(data => {
    if (err.value) {
      errorMessage.value = data.message;
      console.log(errorMessage.value);
    }
    else{
      router.push('/login'); // Redirect to the login page upon successful registration
    }
    console.log(data);
  })
  .catch(error => {
    // Handle any errors that might occur during the API call
    console.error(error);
    err.value = true;
    errorMessage.value = 'An error occurred. Please try again later.';
  });
};

</script>
 