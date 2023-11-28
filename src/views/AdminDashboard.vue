<template>
  <div>
    <h1>
      Hello Admin

    </h1>
    <p>🛑Click on a theater name to view its details</p>

    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Place</th>
          <th>Capacity</th>
          <th>Edit</th>
          <th>Delete</th>
          <th>Export in CSV</th> 
        </tr>
      </thead>
      <tbody>
        <!-- Use v-for to iterate over the theatres data -->
        <tr v-for="theatre in theatres" :key="theatre.id">
          <td>{{ theatre.id }}</td>
          <td>
            <router-link :to="{ path: `/admin/${theatre.id}/${theatre.name}/viewShows` }">
              {{ theatre.name }}
            </router-link>
          </td>
          <td>{{ theatre.place }}</td>
          <td>{{ theatre.capacity }}</td>
          <td>
            <!-- Link to the edit page with the theatre ID as a parameter -->
            <router-link :to="{ path: `/admin/${theatre.id}/editTheatre`, state: { theatreData: theatre } }">Edit</router-link>
          </td>
          <td>
            <!-- Button to handle the deletion -->
            <button @click="showDeleteConfirmation(theatre.id)">Delete</button>
          </td>
          <td>
            <!-- Button to handle the deletion -->
            <button @click="export_csv(theatre.id)">Export</button>
          </td>
        </tr>
      </tbody>
    </table>
    <div v-if="showConfirmDialog">
        <p>Are you sure you want to delete this theatre?</p>
          <button @click="deleteTheatreConfirmed(theatreToDelete)">Confirm</button>
          <button @click="cancelDelete">Cancel</button>
    </div>
    <br>
    <div>
      <router-link to="/admin/createTheatre">
        <button>Create New Theatre</button>
      </router-link>
    </div>

  <p v-if="err" style="color: red">{{ errorMessage }}</p>
  <div v-if="isFileReady">
      <p>CSV file generated and ready for download!</p>
      <a :href="csvFileLink" download target="_blank">Download CSV</a>
  </div>
  <br>
  <div>
      <router-link to="/login">
        <button>Login as a different user</button>
      </router-link>
    </div>
</div>
</template>


<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

// Data properties
const theatres = ref([]);
const errorMessage = ref('');
const err= ref(false);
const isFileReady = ref(false);
const csvFileLink = ref('');
const showConfirmDialog = ref(false);
const theatreToDelete = ref(null);
// Fetch theatres function

const fetchtheatres = () => {
  // Get the access token from local storage
  const accessToken = localStorage.getItem('accessToken');

  // Check if the access token is available
  // if (!accessToken) {
  //   router.push('/login');
  //   return;
  // }

  // Make the GET request to the API with the access token in the header
  fetch('http://127.0.0.1:5000/api/admin/theatres', {
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
      errorMessage.value = 'An error occurred while fetching theatres.';
    });
};


// Function to delete a theatre based on its ID
const showDeleteConfirmation = (theatreId) => {
  showConfirmDialog.value = true;
  theatreToDelete.value = theatreId;
};
const cancelDelete = () => {
  showConfirmDialog.value = false;
};
const deleteTheatreConfirmed = (theatreId) => {
  const accessToken = localStorage.getItem('accessToken');
  if (!accessToken) {
    // Handle the situation when the access token is not available (e.g., redirect to login page)
    console.error('Access token not found. Redirect to login page or handle the error.');
    return;
  }

  fetch(`http://127.0.0.1:5000/api/theatre/${theatreId}`, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${accessToken}`
    }
  })
  .then(response => {
      if (!response.ok) {
        console.error('Error deleting theatre:', response.statusText);
        // Handle error response, if needed
      } else {
        console.log('Theatre deleted successfully!');
        // Perform any actions after successful deletion, if needed
        // For example, you can fetch theatres again to update the table
        showConfirmDialog.value = false;
        fetchtheatres();
      }
    })
    .catch(error => {
      console.error('Error deleting theatre:', error);
    });
}
const export_csv= (theatreId) => {
  fetch(`http://127.0.0.1:5000/admin/export_csv/${theatreId}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      // 'Authorization': `Bearer ${accessToken}`
    }
  })
  .then(response => {
    if (!response.ok){
      err.value=true;
    }
    else{
      isFileReady.value = true;
      csvFileLink.value= `http://127.0.0.1:5000/download_csv/${theatreId}`
      err.value=false;
    }
    // console.log(err.value);
    return response.json();
  })
  .then(data => {
      if (!err.value) {
        // console.log("err= false");
        // Display a success message using alert
        alert('Success: ' + data.message);
      } else {
        // Display an error message using alert
        alert('Error: ' + data.message);
      }
    })
    .catch(error => {
      // Display an error message using alert
      alert('An error occurred: ' + error.message);
    })
}

// Call the fetchtheatres function when the component is mounted
onMounted(fetchtheatres);

// fetchtheatres();
</script>
