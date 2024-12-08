<script>
import {
  createPersonalNotes,
  deletePersonalNotes,
} from "./personal_notes.graphql";
import personalNoteRelatedMixin from "./personalNoteRelatedMixin";
import mutateMixin from "aleksis.core/mixins/mutateMixin.js";

export default {
  name: "ExtraMarkNoteCheckbox",
  mixins: [mutateMixin, personalNoteRelatedMixin],
  props: {
    personalNote: {
      type: Object,
      default: null,
    },
    /**
     * Extra Mark
     */
    value: {
      type: Object,
      required: true,
    },
  },
  computed: {
    model: {
      get() {
        return !!this.personalNote?.id;
      },
      set(newValue) {
        if (newValue && !this.personalNote) {
          // CREATE new personal note
          this.mutate(
            createPersonalNotes,
            {
              input: [
                {
                  documentation: this.documentation.id,
                  person: this.participation.person.id,
                  extraMark: this.value.id,
                },
              ],
            },
            (storedDocumentations, incomingPersonalNotes) => {
              const note = incomingPersonalNotes[0];
              const documentation = storedDocumentations.find(
                (doc) => doc.id === this.documentation.id,
              );
              const participationStatus = documentation.participations.find(
                (part) => part.id === this.participation.id,
              );
              participationStatus.notesWithExtraMark.push(note);

              return storedDocumentations;
            },
          );
        } else {
          // DELETE personal note
          this.mutate(
            deletePersonalNotes,
            {
              ids: [this.personalNote.id],
            },
            (storedDocumentations) => {
              const documentation = storedDocumentations.find(
                (doc) => doc.id === this.documentation.id,
              );
              const participationStatus = documentation.participations.find(
                (part) => part.id === this.participation.id,
              );
              const index = participationStatus.notesWithExtraMark.findIndex(
                (n) => n.id === this.personalNote.id,
              );
              participationStatus.notesWithExtraMark.splice(index, 1);

              return storedDocumentations;
            },
          );
        }
      },
    },
  },
};
</script>

<template>
  <v-checkbox
    :label="value.name"
    :value="value.id"
    v-model="model"
    :disabled="$attrs?.disabled || loading"
    :true-value="true"
    :false-value="false"
  >
    <template #append>
      <v-progress-circular
        v-if="loading"
        indeterminate
        :size="16"
        :width="2"
      ></v-progress-circular>
    </template>
  </v-checkbox>
</template>
