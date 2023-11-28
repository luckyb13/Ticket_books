<template>
    <div>
        <h1>Shows for {{ theatre_name }}</h1>
        <table>
        <thead>
          <tr>
            <th>Id</th>
            <th>Name</th>
            <th>Rating</th>
            <th>Tags</th>
            <th>Ticket Price</th>
            <th>Start Time</th>
            <th>End Time</th>
            <th>Edit</th>
            <th>Delete</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="show in shows" :key="show.id">
            <td>{{ show.id }}</td>
            <td>{{ show.name }}</td>
            <td>{{ show.rating }}</td>
            <td>{{ show.tags }}</td>
            <td>{{ show.ticket_price }}</td>
            <td>{{ show.start_time_hours }}:{{ show.start_time_minutes }}</td>
            <td>{{ show.end_time_hours }}:{{ show.end_time_minutes }}</td>
          <td>
            <router-link :to="{ path: `/admin/${theatre_id}/${theatre_name}/${show.id}/editShow`}">Edit</router-link>
          </td>
          <td>
            <button @click="showDeleteConfirmation(show.id)">Delete</button>
          </td>
          </tr>
        </tbody>
      </table>
      <div v-if="showConfirmDialog">
        <p>Are you sure you want to delete this show?</p>
          <button @click="deleteShowConfirmed(showToDelete)">Confirm</button>
          <button @click="cancelDelete">Cancel</button>
    </div>
    <br>
      <div>
        <router-link :to="{ path: `/admin/${theatre_id}/${theatre_name}/createShow`}">
          <button>Create New Show</button>
      </router-link>
      <br>
      <br>
      </div>
          <div>
        <router-link :to="{ path: `/admin/dashboard`}">
          <button>Go to admin dashboard</button>
      </router-link>
      </div>

    </div>
</template>
  
<script setup>
  import { ref, onMounted } from 'vue';
  import { useRoute } from 'vue-router';
  import { useRouter } from 'vue-router';
const router = useRouter();
  const route = useRoute();
  
  const shows = ref([]);
  const theatre_id = route.params.id;
  const theatre_name= route.params.theatreName;
  // console.log(theatre_name);  
  const showConfirmDialog = ref(false);
  const showToDelete = ref(null);

  const accessToken = localStorage.getItem('accessToken');
  
  const fetchData = () => {
    const url = `http://localhost:5000/api/${theatre_id}/shows`;
    const headers = new Headers();
    headers.append('Authorization', `Bearer ${accessToken}`);
  
    fetch(url, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${accessToken}`
    }
  })
      .then((response) => response.json())
      .then((data) => {
        shows.value = data;
      })
      .catch((error) => {
        console.error('Error fetching data:', error);
      });
  };

const showDeleteConfirmation = (showId) => {
  showConfirmDialog.value = true;
  showToDelete.value = showId;
};
const cancelDelete = () => {
  showConfirmDialog.value = false;
}

const deleteShowConfirmed = (show_id) => {
  const accessToken = localStorage.getItem('accessToken');
  if (!accessToken) {
    // Handle the situation when the access token is not available (e.g., redirect to login page)
    console.error('Access token not found. Redirect to login page or handle the error.');
    return;
  }

  fetch(`http://127.0.0.1:5000/api/${theatre_id}/show/${show_id}`, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${accessToken}`
    }
  })
  .then(response => {
      if (!response.ok) {
        console.error('Error deleting show:', response.statusText);
        // Handle error response, if needed
      } else {
        console.log('show deleted successfully!');
        // Perform any actions after successful deletion, if needed
        // For example, you can fetch theatres again to update the table
        showConfirmDialog.value = false;
        fetchData();
      }
    })
    .catch(error => {
      console.error('Error deleting show:', error);
    });
}

  onMounted(() => {
    fetchData();
  });
</script>
  