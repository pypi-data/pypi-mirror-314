<template>
  <v-card outlined dense rounded="lg" v-bind="$attrs" v-on="$listeners">
    <template v-if="documentation.topic">
      <div class="font-weight-medium mr-2">
        {{ $t("alsijil.coursebook.summary.topic.label") }}:
      </div>
      <div class="text-truncate">{{ documentation.topic }}</div>
    </template>

    <template v-if="documentation.homework">
      <div class="font-weight-medium mr-2">
        {{ $t("alsijil.coursebook.summary.homework.label") }}:
      </div>
      <div class="text-truncate">{{ documentation.homework }}</div>
    </template>

    <template v-if="documentation.groupNote">
      <div class="font-weight-medium mr-2">
        {{ $t("alsijil.coursebook.summary.group_note.label") }}:
      </div>
      <div class="text-truncate">{{ documentation.groupNote }}</div>
    </template>
  </v-card>
</template>

<script>
export default {
  name: "DocumentationCompactDetails",
  props: {
    documentation: {
      type: Object,
      required: true,
    },
  },
};
</script>
