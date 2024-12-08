<script setup>
import MobileFullscreenDialog from "aleksis.core/components/generic/dialogs/MobileFullscreenDialog.vue";
import SecondaryActionButton from "aleksis.core/components/generic/buttons/SecondaryActionButton.vue";
import PrimaryActionButton from "aleksis.core/components/generic/buttons/PrimaryActionButton.vue";
import CancelButton from "aleksis.core/components/generic/buttons/CancelButton.vue";
</script>

<template>
  <mobile-fullscreen-dialog v-model="dialog">
    <template #activator>
      <secondary-action-button
        i18n-key="alsijil.coursebook.print.button"
        icon-text="$print"
        :loading="loading"
        @click="dialog = true"
        :disabled="dialog"
      />
    </template>
    <template #title>
      {{ $t("alsijil.coursebook.print.title") }}
    </template>
    <template #content>
      {{ $t("alsijil.coursebook.print.groups") }}
      <v-autocomplete
        :items="availableGroups"
        item-text="name"
        item-value="id"
        :value="value"
        @input="setGroupSelection"
        @click:clear="setGroupSelection"
        multiple
        chips
        deletable-chips
      />
      <div class="d-flex flex-column">
        {{ $t("alsijil.coursebook.print.include") }}
        <v-checkbox
          v-model="includeCover"
          :label="$t('alsijil.coursebook.print.include_cover')"
        />
        <v-checkbox
          v-model="includeAbbreviations"
          :label="$t('alsijil.coursebook.print.include_abbreviations')"
        />
        <v-checkbox
          v-model="includeMembersTable"
          :label="$t('alsijil.coursebook.print.include_members_table')"
        />
        <v-checkbox
          v-model="includeTeachersAndSubjectsTable"
          :label="
            $t('alsijil.coursebook.print.include_teachers_and_subjects_table')
          "
        />
        <v-checkbox
          v-model="includePersonOverviews"
          :label="$t('alsijil.coursebook.print.include_person_overviews')"
        />
        <v-checkbox
          v-model="includeCoursebook"
          :label="$t('alsijil.coursebook.print.include_coursebook')"
        />
      </div>
    </template>
    <template #actions>
      <!-- TODO: Should cancel reset state? -->
      <cancel-button @click="dialog = false" />
      <primary-action-button
        i18n-key="alsijil.coursebook.print.button"
        icon-text="$print"
        :disabled="!valid"
        @click="print"
      />
    </template>
  </mobile-fullscreen-dialog>
</template>

<script>
/**
 * This component provides a dialog for configuring the coursebook-printout
 */
export default {
  name: "CoursebookPrintDialog",
  props: {
    /**
     * Groups available for selection
     */
    availableGroups: {
      type: Array,
      required: true,
    },
    /**
     * Initially selected groups
     */
    value: {
      type: Array,
      required: false,
      default: () => [],
    },
    /**
     * Loading state
     */
    loading: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  emits: ["input"],
  data() {
    return {
      dialog: false,
      currentGroupSelection: [],
      includeCover: true,
      includeAbbreviations: true,
      includeMembersTable: true,
      includeTeachersAndSubjectsTable: true,
      includePersonOverviews: true,
      includeCoursebook: true,
    };
  },
  computed: {
    selectedGroups() {
      if (this.currentGroupSelection.length == 0) {
        return this.value.map((group) => group.id);
      } else {
        return this.currentGroupSelection;
      }
    },
    valid() {
      return (
        this.selectedGroups.length > 0 &&
        (this.includeMembersTable ||
          this.includeTeachersAndSubjectsTable ||
          this.includePersonOverviews ||
          this.includeCoursebook)
      );
    },
  },
  methods: {
    setGroupSelection(groups) {
      this.$emit("input", groups);
      this.currentGroupSelection = groups;
    },
    print() {
      this.$router.push({
        name: "alsijil.coursebook_print",
        params: {
          groupIds: this.selectedGroups,
        },
        query: {
          cover: this.includeCover,
          abbreviations: this.includeAbbreviations,
          members_table: this.includeMembersTable,
          teachers_and_subjects_table: this.includeTeachersAndSubjectsTable,
          person_overviews: this.includePersonOverviews,
          coursebook: this.includeCoursebook,
        },
      });
    },
  },
};
</script>
