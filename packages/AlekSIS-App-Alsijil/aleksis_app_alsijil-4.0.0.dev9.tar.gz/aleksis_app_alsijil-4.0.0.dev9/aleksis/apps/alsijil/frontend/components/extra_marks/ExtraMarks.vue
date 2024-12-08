<script setup>
import ColorField from "aleksis.core/components/generic/forms/ColorField.vue";
import InlineCRUDList from "aleksis.core/components/generic/InlineCRUDList.vue";
</script>

<template>
  <v-container>
    <inline-c-r-u-d-list
      :headers="headers"
      :i18n-key="i18nKey"
      create-item-i18n-key="alsijil.extra_marks.create"
      :gql-query="gqlQuery"
      :gql-create-mutation="gqlCreateMutation"
      :gql-patch-mutation="gqlPatchMutation"
      :gql-delete-mutation="gqlDeleteMutation"
      :default-item="defaultItem"
    >
      <!-- eslint-disable-next-line vue/valid-v-slot -->
      <template #name.field="{ attrs, on }">
        <div aria-required="true">
          <v-text-field
            v-bind="attrs"
            v-on="on"
            :rules="$rules().required.build()"
          />
        </div>
      </template>

      <!-- eslint-disable-next-line vue/valid-v-slot -->
      <template #shortName.field="{ attrs, on }">
        <div aria-required="true">
          <v-text-field
            v-bind="attrs"
            v-on="on"
            :rules="$rules().required.build()"
          />
        </div>
      </template>

      <template #colourFg="{ item }">
        <v-chip :color="item.colourFg" outlined v-if="item.colourFg">
          {{ item.colourFg }}
        </v-chip>
        <span v-else>–</span>
      </template>
      <!-- eslint-disable-next-line vue/valid-v-slot -->
      <template #colourFg.field="{ attrs, on }">
        <color-field v-bind="attrs" v-on="on" />
      </template>

      <template #colourBg="{ item }">
        <v-chip :color="item.colourBg" outlined v-if="item.colourBg">
          {{ item.colourBg }}
        </v-chip>
        <span v-else>–</span>
      </template>
      <!-- eslint-disable-next-line vue/valid-v-slot -->
      <template #colourBg.field="{ attrs, on }">
        <color-field v-bind="attrs" v-on="on" />
      </template>

      <template #showInCoursebook="{ item }">
        <v-switch
          :input-value="item.showInCoursebook"
          disabled
          inset
          :false-value="false"
          :true-value="true"
        />
      </template>
      <!-- eslint-disable-next-line vue/valid-v-slot -->
      <template #showInCoursebook.field="{ attrs, on }">
        <v-switch
          v-bind="attrs"
          v-on="on"
          inset
          :false-value="false"
          :true-value="true"
          :hint="$t('alsijil.extra_marks.show_in_coursebook_helptext')"
          persistent-hint
        />
      </template>
    </inline-c-r-u-d-list>
  </v-container>
</template>

<script>
import formRulesMixin from "aleksis.core/mixins/formRulesMixin.js";
import {
  extraMarks,
  createExtraMarks,
  deleteExtraMarks,
  updateExtraMarks,
} from "./extra_marks.graphql";

export default {
  name: "ExtraMarks",
  mixins: [formRulesMixin],
  data() {
    return {
      headers: [
        {
          text: this.$t("alsijil.extra_marks.short_name"),
          value: "shortName",
        },
        {
          text: this.$t("alsijil.extra_marks.name"),
          value: "name",
        },
        {
          text: this.$t("alsijil.extra_marks.colour_fg"),
          value: "colourFg",
        },
        {
          text: this.$t("alsijil.extra_marks.colour_bg"),
          value: "colourBg",
        },
        {
          text: this.$t("alsijil.extra_marks.show_in_coursebook"),
          value: "showInCoursebook",
        },
      ],
      i18nKey: "alsijil.extra_marks",
      gqlQuery: extraMarks,
      gqlCreateMutation: createExtraMarks,
      gqlPatchMutation: updateExtraMarks,
      gqlDeleteMutation: deleteExtraMarks,
      defaultItem: {
        shortName: "",
        name: "",
        colourFg: "",
        colourBg: "",
        showInCoursebook: true,
      },
    };
  },
};
</script>
