<script>
import {
  createPersonalNotes,
  deletePersonalNotes,
  updatePersonalNotes,
} from "./personal_notes.graphql";
import personalNoteRelatedMixin from "./personalNoteRelatedMixin";
import mutateMixin from "aleksis.core/mixins/mutateMixin.js";
import DeleteDialog from "aleksis.core/components/generic/dialogs/DeleteDialog.vue";

export default {
  name: "TextNote",
  components: { DeleteDialog },
  mixins: [mutateMixin, personalNoteRelatedMixin],
  props: {
    value: {
      type: Object,
      required: true,
    },
  },
  computed: {
    model: {
      get() {
        return this.value.note;
      },
      set(newValue) {
        if (!newValue) {
          // this is a DELETE action, show the dialog, ...
          this.showDeleteConfirm = true;
          return;
        }
        const create = !this.value.id;

        this.mutate(
          create ? createPersonalNotes : updatePersonalNotes,
          this.getInput(
            newValue,
            create
              ? {
                  documentation: this.documentation.id,
                  person: this.participation.person.id,
                  extraMark: null,
                }
              : {
                  id: this.value.id,
                },
          ),
          this.getUpdater(create ? "create" : "update"),
        );
      },
    },
  },
  methods: {
    getInput(newValue, extras) {
      return {
        input: [
          {
            note: newValue,
            ...extras,
          },
        ],
      };
    },
    getUpdater(mode) {
      return (storedDocumentations, incomingPersonalNotes) => {
        const note = incomingPersonalNotes?.[0] || undefined;
        const documentation = storedDocumentations.find(
          (doc) => doc.id === this.documentation.id,
        );
        const participationStatus = documentation.participations.find(
          (part) => part.id === this.participation.id,
        );
        switch (mode.toLowerCase()) {
          case "update":
          case "delete": {
            const updateIndex = participationStatus.notesWithNote.findIndex(
              (n) => n.id === this.value.id,
            );
            if (mode === "update") {
              participationStatus.notesWithNote.splice(updateIndex, 1, note);
            } else {
              participationStatus.notesWithNote.splice(updateIndex, 1);
            }

            break;
          }

          case "create":
            participationStatus.notesWithNote.push(note);

            this.$emit("create");
            break;

          default:
            console.error("Invalid mode in getUpdater():", mode);
            break;
        }

        return storedDocumentations;
      };
    },
  },
  data() {
    return {
      showDeleteConfirm: false,
      deletePersonalNotes,
    };
  },
};
</script>

<template>
  <v-textarea
    auto-grow
    :rows="3"
    outlined
    hide-details
    class="mb-4"
    :label="$t('alsijil.personal_notes.note')"
    :value="model"
    @change="model = $event"
    :loading="loading"
  >
    <template #append>
      <v-slide-x-reverse-transition>
        <v-btn
          v-if="!!model"
          icon
          @click="showDeleteConfirm = true"
          class="mt-n1-5"
        >
          <v-icon> $deleteContent </v-icon>
        </v-btn>
      </v-slide-x-reverse-transition>

      <delete-dialog
        v-model="showDeleteConfirm"
        :gql-delete-mutation="deletePersonalNotes"
        :affected-query="affectedQuery"
        item-attribute="fullName"
        :items="[value]"
        :custom-update="getUpdater('delete')"
      >
        <template #title>
          {{ $t("alsijil.personal_notes.confirm_delete") }}
        </template>
        <template #body>
          {{
            $t("alsijil.personal_notes.confirm_delete_explanation", {
              note: value.note,
              name: participation.person.fullName,
            })
          }}
        </template>
      </delete-dialog>
    </template>
  </v-textarea>
</template>

<style scoped>
.mt-n1-5 {
  margin-top: -6px;
}
</style>
