<template>
  <div class="flex w-full">
    <div v-if="!tbc || isLocation" class="w-11/12">
      <SelectIndicatorField
        v-if="!tbc || isLocation"
        v-bind="$attrs"
        :filterable="false"
        :options="airportLocations"
        :reduce="(item: any) => ({
        id: item.id,
        full_repr: item.full_repr,
        tiny_repr: item.tiny_repr,
        is_lat_lon_available: item.is_lat_lon_available,
        country: item.country.name
      })
        "
        :indicator-value="country"
        :loading="isLoadingAirportLocations"
        label="full_repr"
        @search="onSearchAirports"
        @update:model-value="onChange"
      >
        <template #no-options>Search location by Name/ICAO/IATA</template>
      </SelectIndicatorField>
    </div>
    <div v-if="tbc && !isLocation" class="w-11/12">
      <SelectField
        v-if="tbc && !isLocation"
        v-model="int_dom"
        class="w-11/12"
        label-text="Destination Airport:"
        placeholder="Please select type"
        label="name"
        is-validation-dirty
        :errors="intDomError"
        :options="[
          { code: 'INT', name: 'International' },
          { code: 'DOM', name: 'Domestic' }
        ]"
        :loading="false"
      />
    </div>
    <div v-if="!isLocation" class="flex items-center justify-end w-1/12 mt-[1rem]">
      <CheckboxField v-model="tbc" class="mb-0 mr-[0.25rem]" :size="'24px'" />
      <p class="text-base whitespace-nowrap">TBC</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, useAttrs, watch } from 'vue';
import { useDebounceFunction, useFetch } from 'shared/composables';
import { useOrderFormStore } from '@/stores/useOrderFormStore';
import { useOrderStore } from '@/stores/useOrderStore';
import orderReferences from '@/services/order/order-references';
import CheckboxField from '../forms/fields/CheckboxField.vue';
import SelectField from '../forms/fields/SelectField.vue';
import SelectIndicatorField from '../forms/fields/SelectIndicatorField.vue';

import type { IAirport } from 'shared/types';

const attrs = useAttrs();
const props = defineProps({
  isTbc: {
    type: Boolean,
    default: false
  },
  isLocation: {
    type: Boolean,
    default: false
  },
  intDomError: {
    type: String,
    default: () => null
  }
});

const {
  loading: isLoadingAirportLocations,
  data: airportLocations,
  callFetch: fetchAirportLocations
} = useFetch<IAirport[]>(async (search?: string) => {
  return await orderReferences.fetchAirportLocations(search);
});

const orderStore = useOrderStore();
const { formModel } = useOrderFormStore();

const country = ref(
  props.isLocation
    ? orderStore.locationCountry
    : orderStore.destinationCountry
    ? orderStore.isLocal
      ? 'Domestic'
      : 'International'
    : ''
);

const debounce = useDebounceFunction();
const tbc = ref(props.isTbc);
const int_dom = ref();

const onChange = async (event: any) => {
  if (event) {
    if (props.isLocation) {
      orderStore.locationCountry = event.country;
      country.value = orderStore.locationCountry;
    } else {
      orderStore.destinationCountry = event.country;
      country.value = orderStore.isLocal ? 'Domestic' : 'International';
      if (tbc.value) {
        formModel.destination_int_dom = orderStore.isLocal
          ? { code: 'DOM', name: 'Domestic' }
          : { code: 'INT', name: 'International' };
        formModel.destination = null;
      } else {
        formModel.destination_int_dom = null;
      }
    }
    return;
  }
  await fetchAirportLocations();
};

const onSearchAirports = (event: string) =>
  debounce(async () => {
    if (attrs.modelValue && !event) return;
    await fetchAirportLocations(event as any);
  });

watch(
  () => tbc.value,
  (tbc) => {
    if (tbc) {
      formModel.destination = null;
    }
  }
);

watch(
  () => int_dom.value,
  (int_dom) => {
    formModel.destination_int_dom = int_dom;
    if (int_dom) formModel.destination = null;
  }
);

watch(
  () => props.isTbc,
  (value) => {
    int_dom.value = formModel.destination_int_dom;
    tbc.value = value;
  },
  { immediate: true }
);
</script>
