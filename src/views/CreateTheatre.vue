<template>
    <div>
      <h2>Create New Theatre</h2>
      <form @submit.prevent="handleCreateTheatre">
        <label for="name">Name: </label>
        <input type="text" id="name" v-model="name" required />
        <br />
        <br />
        <label for="place">Place: </label>
        <input type="text" id="place" v-model="place" required />
        <br />
        <br />
        <label for="capacity">Capacity: </label>
        <input type="number" id="capacity" v-model="capacity" required />
        <br />
        <br />
        <button type="submit">Submit</button>
      </form>
    </div>
    <p v-if="err" style="color: red">{{ errorMessage }}</p>
    <br>
    <div>
        <router-link :to="{ path: `/admin/dashboard`}">
          <button>Go back</button>
      </router-link>
      </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import { useRouter } from 'vue-router';
  const router = useRouter();
  // Data properties for the form inputs
  const name = ref('');
  const place = ref('');
  const capacity = ref('');
  const errorMessage = ref('');
  const err= ref(false);
  // Function to handle theatre creation
  const handleCreateTheatre = () => {
    const accessToken = localStorage.getItem('accessToken');
    if (!accessToken) {
      // Handle the situation when access token is not available (e.g., redirect to login page)
      console.error('Access token not found. Redirect to login page or handle the error.');
      return;
    }
  
    const theatreData = {
      name: name.value,
      place: place.value,
      capacity: capacity.value
    };
  
    fetch('http://localhost:5000/api/admin/theatres', {
      method: 'POST',
      body: JSON.stringify(theatreData),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`
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
      router.push('/admin/dashboard'); // Redirect to the login page upon successful registration
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
  