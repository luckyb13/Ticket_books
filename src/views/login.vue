<template>
    <div>
      <h2>Login Form</h2>
      <form @submit.prevent="handleLogin">
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
        <button type="submit">Login </button>
      </form>
      <!-- <p v-if="error" style="color: red">{{ error }}</p> -->
      <p v-if="err" style="color: red">{{ errorMessage }}</p>
    </div>
  </template>
  
  <script setup>
    import { ref } from 'vue';
    import { useRouter } from 'vue-router';
  
    const router = useRouter();
    const usernameInput = ref(null);
    const passwordInput = ref(null);
    const username = ref('');
    const password = ref('');
    // const error = ref('');
    const user_id= ref('');
    const errorMessage = ref('');
    const err= ref(false);

    // Function to handle sign up
    const handleLogin = () => {
      // If the form is invalid, the browser will handle the validation and display errors
      if (!usernameInput.value.validity.valid || !passwordInput.value.validity.valid) {
        return;
      }
      const userData = {
      "username": username.value,
      "password": password.value
      }
    //   // For this example, we'll just log the values to the console
        console.log('Username:', username.value);
        console.log('Password:', password.value);
      
      fetch('http://127.0.0.1:5000/api/login', {
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
          return response.json().then(data => {
            localStorage.setItem('accessToken', data.access_token);
            return data;
          });
        }
      })
      .then(data => {
      if (err.value) {
        errorMessage.value = data.message;
        console.log(errorMessage.value);
      } else {
        console.log(data);
        // Get the user_id and username from the data
        // Navigate to the appropriate dashboard based on the username
        if (username.value=== 'admin') {
          router.push('/admin/dashboard');
        } else {
          router.push(`/user/${data.id}/${username.value}/dashboard`);
        }
      }
    })
    .catch(error => {
      console.error(error);
      err.value = true;
      errorMessage.value = 'An error occurred. Please try again later.';
    });
};
  </script>
  