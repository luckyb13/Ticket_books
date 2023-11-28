<template>
    <div>
      <h2>Edit Theatre</h2>
      <form @submit.prevent="handleEditTheatre">
        <label for="name">Name: </label>
        <input type="text" id="name" ref="nameInput" v-model="name" required />
        <br />
  
        <label for="place">Place: </label>
        <input type="text" id="place" ref="placeInput" v-model="place" required />
        <br />
  
        <label for="capacity">Capacity: </label>
        <input type="number" id="capacity" ref="capacityInput" v-model="capacity" required />
        <br />
  
        <button type="submit"  @click="handleEditTheatre">Save Changes</button>
      </form>
      <br>
      <div>
        <router-link :to="{ path: `/admin/dashboard`}">
          <button>Go back</button>
      </router-link>
      </div>
    </div>
</template>
  
<script setup>
  import { ref, onMounted } from 'vue';
  import { useRouter } from 'vue-router';
  import { useRoute } from 'vue-router';
  const route = useRoute();
  const router = useRouter();
//   const theatreId = ref(null);
  const name = ref('');
  const place = ref('');
  const capacity = ref('');
  const theatre_id = route.params.id;
  console.log(theatre_id);
  const nameInput = ref(null);
  const placeInput = ref(null);
  const capacityInput = ref(null);
    


  // Function to handle theatre update
  const handleEditTheatre = () => {
    if (!nameInput.value.validity.valid || !placeInput.value.validity.valid || !capacityInput.value.validity.valid) {
    return;
  }
    const accessToken = localStorage.getItem('accessToken');
    
    if (!accessToken) {
        // Handle the situation when access token is not available (e.g., redirect to login page)
        console.error('Access token not found. Redirect to login page or handle the error.');
        return;
    }

    const updatedTheatreData = {
      name: name.value,
      place: place.value,
      capacity: capacity.value
    };
  
    
  // Send the PUT request to the API endpoint to update the theatre data
  fetch(`http://localhost:5000/api/theatre/${theatre_id}`, {
    method: 'PUT',
    body: JSON.stringify(updatedTheatreData),
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${accessToken}`
    }
  })
    .then(response => {
      if (!response.ok) {
        console.error('Error updating theatre:', response.statusText);
        // Handle error response, if needed
      } else {
        console.log('Theatre updated successfully!');
        // Perform any actions after successful update, if needed
        // For example, you can navigate back to the AdminDashboard
        router.push('/admin/dashboard');
      }
    })
    .catch(error => {
      console.error('Error updating theatre:', error);
    });
};
  
  // Fetch the theatre details when the component is mounted
//   onMounted(() => {
//     // Get the theatre ID from the route params
//     theatreId.value = $route.params.theatreId;
//     // Fetch theatre details based on the ID
//     fetchTheatreDetails();
//   });
</script>
  