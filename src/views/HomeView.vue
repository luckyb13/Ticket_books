<!-- LandingPage.vue -->
<!-- LandingPage.vue -->
<template>
  <div>
    <!-- <h1>Welcome to our Landing Page!</h1> -->
    <nav>
      <router-link class="link" to="/login">Login</router-link>   |   
      <router-link class="link" to="/register">Register</router-link>
    </nav>
    <p>
      🛑If you are an admin or an existing user, click on login
    </p>
    <p>
      🛑If you are a new user, click on register
    </p>
  </div>
</template>

<!-- ... Rest of the components as shown above ... -->

<script>
export default {

}
</script>


<style>
.link {
  font-size: 30px; /* Adjust the font size as per your preference */
  /* Add any other styles you want to customize the appearance of the links */
}
</style>