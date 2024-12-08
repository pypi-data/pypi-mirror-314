<template>
  <v-card class="my-2 full-width">
    <div class="full-width d-flex flex-column align-stretch flex-md-row">
      <v-card-text>
        <v-skeleton-loader
          type="avatar, heading, chip"
          class="d-flex full-width align-center gap"
          height="100%"
        />
      </v-card-text>
      <v-card-text>
        <v-skeleton-loader
          type="heading@2"
          class="d-flex full-width align-center gap"
          height="100%"
        />
      </v-card-text>
      <v-card-text>
        <v-skeleton-loader
          type="chip@3"
          class="d-flex full-width align-center justify-end gap"
          height="100%"
        />
      </v-card-text>
    </div>
  </v-card>
</template>
<script>
export default {
  name: "DocumentationLoader",
};
</script>
