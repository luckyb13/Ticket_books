<template>
    <div>
      <h1>All theatres</h1>
      <input
      type="text"
      v-model="searchTerm"
      placeholder="Search by place"
    />
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
          <tr v-for="theatre in filteredTheatres" :key="theatre.id">
            <td>{{ theatre.id }}</td>
            <td>{{ theatre.name }}</td>
            <td>{{ theatre.place }}</td>
            <td>{{ theatre.capacity }}</td>
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
    import { ref, onMounted, computed } from 'vue';
    import { useRouter } from 'vue-router';
    
    import { useRoute } from 'vue-router';
    const route = useRoute();
    const router = useRouter();

    const username = route.params.username;
    const user_id= route.params.id;
    // Data properties
    const theatres = ref([]);
    const searchTerm = ref('');
    const errorMessage = ref('');
    const err= ref(false);
    
    // Fetch theatres function 
    //function   
    const fetchtheatres = () => {
        // Get the access token from local storage
        const accessToken = localStorage.getItem('accessToken');
    
        // Check if the access token is available
        // if (!accessToken) {
        //   router.push('/login');
        //   return;
        // }
    
        // Make the GET request to the API with the access token in the header
        fetch(`http://127.0.0.1:5000/api/user/${user_id}/theatres`, {
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
            theatres.value = data;
            console.log(theatres.value);
        }
            // Update the theatres data with the response      
        })
        .catch(error => {
            console.error(error);
            err.value = true;
            errorMessage.value = 'An error occurred while fetching theatres for the user.';
        });
    };
    const filteredTheatres = computed(() => {
      if (!searchTerm.value) {
        return theatres.value; // Show all theatres if no search term
      }
      return theatres.value.filter(theatre => theatre.place.toLowerCase() === searchTerm.value.toLowerCase());
    });
    // Call the fetchtheatres function when the component is mounted
    onMounted(fetchtheatres);
</script>
  