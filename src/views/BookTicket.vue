<template>
  <div>
    <h1>Book a ticket for the show: {{ show_name }}</h1>
    <div>
    <form @submit.prevent="bookTicket">
      <div>
          <label for="tickets">Number of Tickets:</label>
      <input type="text" v-model="showData.number_of_tickets" id="tickets" required />

      </div>
      <button type="submit">Book</button>
    </form>
  </div>
  <p v-if="err" style="color: red">{{ errorMessage }}</p>
  <h2>
        <router-link :to="{ path: `/user/${user_id}/${username}/dashboard`}">Go to your dashboard</router-link>
  </h2>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useRoute } from 'vue-router';

const router = useRouter();
const route = useRoute();

const showData = ref({
number_of_tickets: 0,
});
  const accessToken = localStorage.getItem('accessToken');
  const user_id = route.params.id;
  const username= route.params.username;
  const show_id = route.params.show_id;
  const show_name= route.params.show_name;
  const errorMessage = ref('');
  const err= ref(false);

const bookTicket= () => {
 // Validity check: Check if required input values are not empty
 console.log(showData.value);
 if (!showData.value.number_of_tickets) {
  // alert('Please fill in all required fields.');
  return;
}
const url = `http://localhost:5000/api/user/${user_id}/${show_id}/ticketBookings`;
fetch(url, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${accessToken}`,
  },
  body: JSON.stringify(showData.value),
})
  // .then((response) => {
  // if(response.ok){
  //   router.push(`/user/${user_id}/${user_name}/dashboard`); 
  // }
  //   return  response.json()
  // })
  .then(response => {
    if (!response.ok) {
      err.value = true;
      return response.json();
    } else {
      err.value = false;
      console.log("Booking successful");
      return response.json();
    }
  })
  .then(data => {
    if (err.value) {
      errorMessage.value = data.message;
      console.log(errorMessage.value);
    }
    else{
      router.push(`/user/${user_id}/${username}/dashboard`); 
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
