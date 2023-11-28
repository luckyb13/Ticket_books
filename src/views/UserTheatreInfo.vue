<template>
    <div>
      <h1>Theatre Info</h1>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Place</th>
            <th>Capacity</th>
          </tr>
        </thead>
        <tbody>
          <!-- Use v-for to iterate over the theatres data -->
          <!-- <tr v-for="theatre in Theatre" :key="theatre.id"> -->
            <tr>
                <td>{{ Theatre.id }}</td>
                <td>{{ Theatre.name }}</td>
                <td>{{ Theatre.place }}</td>
                <td>{{ Theatre.capacity }}</td>
          </tr>
        </tbody>
      </table>
    <p v-if="err" style="color: red">{{ errorMessage }}</p>
    <h2>
        <router-link :to="{ path: `/user/${user_id}/${username}/dashboard`}">Go to your dashboard</router-link>
    </h2>
  </div>
</template>
  
  
<script setup>
    import { ref, onMounted, computed } from 'vue';
    import { useRouter } from 'vue-router';
    
    import { useRoute } from 'vue-router';
    const route = useRoute();
    const router = useRouter();

    const username = route.params.username;
    const user_id= route.params.id;
    const theatre_id= route.params.theatre_id;
    
    // Data properties
    const Theatre = ref({});
    const errorMessage = ref('');
    const err= ref(false);
    
    // Fetch theatres function 
    const fetchtheatre = () => {
        // Get the access token from local storage
        const accessToken = localStorage.getItem('accessToken');
    
        // Make the GET request to the API with the access token in the header
        fetch(`http://127.0.0.1:5000/api/user/${user_id}/theatre/${theatre_id}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${accessToken}` // Include the access token in the header
        }
        })
        .then(response => {
            // console.log(accessToken);
            return response.json();
        })
        .then(data => {
            if (err.value) {
            errorMessage.value = data.message;
            // console.log(errorMessage.value);
        }
        else{
            console.log(data);
            Theatre.value = data;
            console.log(Theatre.value);
        }
            // Update the theatres data with the response      
        })
        .catch(error => {
            console.error(error);
            err.value = true;
            errorMessage.value = 'An error occurred while fetching theatre for the user.';
        });
    };
    // Call the fetchtheatres function when the component is mounted
    onMounted(fetchtheatre);
</script>
  