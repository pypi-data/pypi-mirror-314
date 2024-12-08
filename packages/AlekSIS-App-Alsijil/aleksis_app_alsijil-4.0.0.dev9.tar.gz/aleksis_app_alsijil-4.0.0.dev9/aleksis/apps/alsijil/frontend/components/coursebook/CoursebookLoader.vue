<template>
  <div>
    <v-list-item v-for="i in numberOfDays" :key="'i-' + i" class="px-0">
      <v-list-item-content>
        <v-list-item-title>
          <v-skeleton-loader type="heading" />
        </v-list-item-title>
        <v-list max-width="100%">
          <v-list-item v-for="j in numberOfDocs" :key="'j-' + j" class="px-1">
            <DocumentationLoader />
          </v-list-item>
        </v-list>
      </v-list-item-content>
    </v-list-item>
  </div>
</template>
<script>
import DocumentationLoader from "./documentation/DocumentationLoader.vue";

export default {
  name: "CoursebookLoader",
  components: { DocumentationLoader },
  props: {
    numberOfDays: {
      type: Number,
      required: false,
      default: 1,
    },
    numberOfDocs: {
      type: Number,
      required: false,
      default: 1,
    },
  },
};
</script>
