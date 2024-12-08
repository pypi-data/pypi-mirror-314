<script setup>
import ExtraMarksNote from "./ExtraMarksNote.vue";
import TextNotes from "./TextNotes.vue";
</script>
<script>
import personalNoteRelatedMixin from "./personalNoteRelatedMixin";

export default {
  name: "PersonalNotes",
  mixins: [personalNoteRelatedMixin],
};
</script>

<template>
  <div>
    <text-notes
      v-bind="personalNoteRelatedProps"
      :value="participation.notesWithNote"
    />

    <extra-marks-note
      v-bind="personalNoteRelatedProps"
      :value="participation.notesWithExtraMark"
    />
  </div>
</template>

<style scoped></style>
