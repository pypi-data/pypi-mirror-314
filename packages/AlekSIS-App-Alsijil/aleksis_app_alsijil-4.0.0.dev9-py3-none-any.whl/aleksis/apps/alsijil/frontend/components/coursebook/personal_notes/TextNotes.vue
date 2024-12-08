<script setup>
import SecondaryActionButton from "aleksis.core/components/generic/buttons/SecondaryActionButton.vue";
import TextNote from "./TextNote.vue";
</script>
<script>
import personalNoteRelatedMixin from "./personalNoteRelatedMixin";

export default {
  name: "TextNotes",
  mixins: [personalNoteRelatedMixin],
  props: {
    value: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      showNewNote: true,
    };
  },
  computed: {
    notes() {
      return this.showNewNote ? [...this.value, { note: "" }] : this.value;
    },
  },
};
</script>

<template>
  <div>
    <text-note
      v-for="note in notes"
      :key="note.id || -1"
      v-bind="personalNoteRelatedProps"
      :value="note"
      @create="showNewNote = false"
    />

    <secondary-action-button
      i18n-key="alsijil.personal_notes.create_personal_note"
      icon-text="$plus"
      class="full-width"
      @click="showNewNote = true"
      :disabled="showNewNote"
    />
  </div>
</template>
