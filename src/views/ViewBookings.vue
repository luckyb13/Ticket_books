<template>
    <div>
      <h1>All bookings</h1>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Show name</th>
            <th>Theatre name</th>
            <th>No. of tickets</th>
            <th>Booking time</th>

        </tr>
        </thead>
        <tbody>
          <!-- Use v-for to iterate over the theatres data -->
          <tr v-for="booking in bookings" :key="booking.id">
            <td>{{ booking.booking_id }}</td>
            <td>{{ booking.show_name }}</td>
            <td>{{ booking.theatre_name }}</td>
            <td>{{ booking.number_of_tickets }}</td>
            <td>{{ booking.booking_time }}</td>

        </tr>
        </tbody>
      </table>
      <!-- <router-link to="/admin/createTheatre">
        <button>Create New Theatre</button>
    </router-link> -->
    <p v-if="err" style="color: red">{{ errorMessage }}</p>
    <h2>
        <router-link :to="{ path: `/user/${user_id}/${username}/dashboard`}">Go to your dashboard</router-link>
    </h2>
  </div>
</template>
  
  
<script setup>
    import { ref, onMounted } from 'vue';
    import { useRouter } from 'vue-router';
    
    import { useRoute } from 'vue-router';
    const route = useRoute();
    const router = useRouter();

    const username = route.params.username;
    const user_id= route.params.id;
    // Data properties
    const bookings = ref([]);
    const errorMessage = ref('');
    const err= ref(false);
    
    // Fetch theatres function 
    //function   
    const fetchbookings = () => {
        // Get the access token from local storage
        const accessToken = localStorage.getItem('accessToken');
    
        // Check if the access token is available
        // if (!accessToken) {
        //   router.push('/login');
        //   return;
        // }
    
        // Make the GET request to the API with the access token in the header
        fetch(`http://127.0.0.1:5000/api/user/${user_id}/bookings`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${accessToken}` // Include the access token in the header
        }
        })
        .then(response => {
            if (!response.ok) {
            err.value = true;
            // console.log(accessToken);
            return response.json();
            }else {
            err.value = false;
            return response.json();
        }
        })
        .then(data => {
            if (err.value) {
            // console.log(data);
            errorMessage.value = data.message;
            // console.log(errorMessage.value);
        }
        else{
            // console.log(data);
            bookings.value = data;
            console.log(bookings.value);
        }
            // Update the theatres data with the response      
        })
        .catch(error => {
            console.error(error);
            err.value = true;
            errorMessage.value = 'An error occurred while fetching bookings for the user.';
        });
    };
    
    // Call the fetchtheatres function when the component is mounted
    onMounted(fetchbookings);
</script>
  