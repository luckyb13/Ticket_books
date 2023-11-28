<template>
    <div>
      <h1>Create a New Show</h1>
      <div>
      <form @submit.prevent="createShow">
        <div>
            <label for="name">Name:</label>
        <input type="text" v-model="showData.name" id="name" required />

        </div>
        <div>
            <label for="rating">Rating:</label>
        <input type="number" v-model="showData.rating" id="rating" required />            
        </div>
        <div>
  
            <label for="tags">Tags:</label>
        <input type="text" v-model="showData.tags" id="tags" required />
            
        </div>
  
        <label for="ticket_price">Ticket Price:</label>
        <input type="number" v-model="showData.ticket_price" id="ticket_price" step="10" required />
  
        <div>
          <label for="start_time_hours">Start Time:</label>
          <input type="number" v-model="showData.start_time_hours" id="start_time_hours" min="0" max="23" placeholder="0-23" required />
          <span>:</span>
          <input type="number" v-model="showData.start_time_minutes" id="start_time_minutes" min="0" max="59" placeholder="0-59" required />
        </div>
  
        <div>
          <label for="end_time_hours">End Time:</label>
          <input type="number" v-model="showData.end_time_hours" id="end_time_hours" min="0" max="23" placeholder="0-23" required/>
          <span>:</span>
          <input type="number" v-model="showData.end_time_minutes" id="end_time_minutes" min="0" max="59" placeholder="0-59" required />
        </div>
  
        <button type="submit">Create Show</button>
      </form>
    </div>
    <br>
    <div>
        <router-link :to="{ path: `/admin/${theatre_id}/${theatre_name}/viewShows`}">
          <button>Go back</button>
      </router-link>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import { useRouter } from 'vue-router';
  import { useRoute } from 'vue-router';

  const router = useRouter();
  const route = useRoute();

  const showData = ref({
  name: '',
  rating: '',
  tags: '',
  ticket_price: '',
  start_time_hours: '',
  start_time_minutes: '',
  end_time_hours: '',
  end_time_minutes: '',
});
    const accessToken = localStorage.getItem('accessToken');
    const theatre_id = route.params.theatre_id;
    const theatre_name= route.params.theatreName;


const createShow = () => {
   // Validity check: Check if required input values are not empty
   console.log(showData.value);
   if (!showData.value.name || !showData.value.rating || !showData.value.tags || !showData.value.ticket_price 
//    || !showData.value.start_time_hours || !showData.value.start_time_minutes || !showData.value.end_time_hours || !showData.value.end_time_minutes
    ) {
    // alert('Please fill in all required fields.');
    return;
  }
  const url = `http://localhost:5000/api/${theatre_id}/shows`;
  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${accessToken}`,
    },
    body: JSON.stringify(showData.value),
  })
    .then((response) => {
    if(response.ok){
      router.push(`/admin/${theatre_id}/${theatre_name}/viewShows`); 
    }
      return  response.json()
    })
    .then((data) => {
      // Handle the response if needed
      console.log('Show created successfully:', data);
    })
    .catch((error) => {
      console.error('Error creating show:', error);
    });
};

  </script>
  
  <!-- <style>
    /* Style the form for better visualization (optional) */
    form {
      display: flex;
      flex-direction: column;
      gap: 10px;
      max-width: 400px;
      margin: 0 auto;
    }
  
    label {
      font-weight: bold;
    }
  
    div {
      display: flex;
      gap: 5px;
    }
  
    div label {
      width: 100px;
    }
  
    div input {
      flex: 1;
    }
  </style>
   -->