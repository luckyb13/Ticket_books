<template>
  <div>
      <h1>Hello {{user_name}}. List of shows for you</h1>
      <h4>🛑Click on Theatre_Id to view its info</h4>
      <input
        type="text"
        v-model="searchTag"
        placeholder="Search by tags"
      />
      <input
        type="text"
        v-model="searchRating"
        placeholder="Rating must be at least"
      />
      <table>
      <thead>
        <tr>
          <th>Book</th>
          <th>Show Id</th>
          <th>Name</th>
          <th>Theatre_Id</th>
          <th>Rating</th>
          <th>Tags</th>
          <th>Ticket Price</th>
          <th>Start Time</th>
          <th>End Time</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="show in filteredShows" :key="show.id">
          <td>
            <router-link :to="{ path: `/user/${user_id}/${user_name}/${show.id}/${show.name}/book`}">Book</router-link>
          </td>
          <td>{{ show.id }}</td>
          <td>{{ show.name }}</td>
          <td>
            <router-link :to="{ path: `/user/${user_id}/${user_name}/theatre/${show.theatre_id}`}">{{ show.theatre_id }}</router-link>
          </td>
          <td>{{ show.rating }}</td>
          <td>{{ show.tags }}</td>
          <td>{{ show.ticket_price }}</td>
          <td>{{ show.start_time_hours }}:{{ show.start_time_minutes }}</td>
          <td>{{ show.end_time_hours }}:{{ show.end_time_minutes }}</td>
        </tr>
      </tbody>
    </table>

    <!-- <router-link :to="{ path: `/admin/${theatre_id}/${theatre_name}/createShow`}">
        <button>Create New Show</button>
    </router-link> -->
<div>
  <h4>
    <router-link :to="{ path: `/user/${user_id}/${user_name}/bookings`}">View all bookings</router-link>
  </h4>
</div>
<!-- <br> -->
<div>
      <router-link :to="{path: `/user/${user_id}/${user_name}/theatres`}">
        <button>View all theatres</button>
      </router-link>
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
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import { useRouter } from 'vue-router';
const router = useRouter();
const route = useRoute();
const shows = ref([]);
const searchTag= ref('');
const searchRating= ref('');
    
const user_id= route.params.id;
const user_name= route.params.username;
const accessToken = localStorage.getItem('accessToken');

const fetchData = () => {
  const url = `http://localhost:5000/api/user/${user_id}/shows`;
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
const filteredShows = computed(() => {
      if (!searchTag.value && !searchRating.value) {
        return shows.value; // Show all theatres if no search term
      }
      return shows.value.filter(show =>{
        // console.log("inside show filtering");
        // console.log(show.rating);
        // console.log(searchRating.value);
      return  show.tags.toLowerCase().includes(searchTag.value.toLowerCase()) &&
      Number(show.rating) >= Number(searchRating.value)
      });
    });
onMounted(() => {
  fetchData();
});
</script>
