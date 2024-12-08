<template>
  <v-card :class="{ 'my-1 full-width': true, 'd-flex flex-column': !compact }">
    <v-card-title v-if="!compact">
      <lesson-information
        v-bind="{ ...$attrs, ...documentationPartProps }"
        :is-create="false"
        :gql-patch-mutation="documentationsMutation"
      />
    </v-card-title>

    <v-card-text
      class="full-width main-body"
      :class="{
        vertical: !compact || $vuetify.breakpoint.mobile,
        'pa-2': compact,
      }"
    >
      <lesson-information
        v-if="compact"
        v-bind="documentationPartProps"
        :is-create="false"
        :gql-patch-mutation="documentationsMutation"
      />
      <lesson-summary
        ref="summary"
        v-bind="{ ...$attrs, ...documentationPartProps }"
        :is-create="false"
        :gql-patch-mutation="documentationsMutation"
        @open="$emit('open')"
        @loading="loading = $event"
        @save="$emit('close')"
        @dirty="dirty = $event"
      />
      <lesson-notes v-bind="documentationPartProps" />
    </v-card-text>
    <v-spacer />
    <v-divider />
    <v-card-actions v-if="!compact">
      <v-spacer />
      <cancel-button
        v-if="documentation.canEdit"
        @click="$emit('close')"
        :disabled="loading"
      />
      <save-button
        v-if="documentation.canEdit"
        @click="save"
        :loading="loading"
        :disabled="!dirty"
      />
      <cancel-button
        v-if="!documentation.canEdit"
        i18n-key="actions.close"
        @click="$emit('close')"
      />
    </v-card-actions>
  </v-card>
</template>

<script>
import LessonInformation from "./LessonInformation.vue";
import LessonSummary from "./LessonSummary.vue";
import LessonNotes from "./LessonNotes.vue";

import SaveButton from "aleksis.core/components/generic/buttons/SaveButton.vue";
import CancelButton from "aleksis.core/components/generic/buttons/CancelButton.vue";

import { createOrUpdateDocumentations } from "../coursebook.graphql";

import documentationPartMixin from "./documentationPartMixin";

export default {
  name: "Documentation",
  components: {
    LessonInformation,
    LessonSummary,
    LessonNotes,
    SaveButton,
    CancelButton,
  },
  emits: ["open", "close", "dirty"],
  mixins: [documentationPartMixin],
  data() {
    return {
      loading: false,
      documentationsMutation: createOrUpdateDocumentations,
      dirty: false,
    };
  },
  methods: {
    save() {
      this.$refs.summary.save();
      this.$emit("close");
    },
  },
  watch: {
    dirty(dirty) {
      this.$emit("dirty", dirty);
    },
  },
};
</script>

<style scoped>
.main-body {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1em;
}
.vertical {
  grid-template-columns: minmax(0, 1fr);
}
</style>
