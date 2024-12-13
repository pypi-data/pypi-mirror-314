<template>
  <div v-if="isOpen" class="order-modal confirm-supplier-modal">
    <div class="order-modal-wrapper">
      <div ref="target" class="order-modal-container">
        <div class="order-modal-body">
          <OrderForm add-default-classes is-modal>
            <template #header>
              <div class="header w-full flex justify-between">
                <div class="text-[1.25rem] font-medium text-grey-1000">Confirm Supplier Order</div>
                <button @click.stop="emit('modal-close')">
                  <img
                    width="12"
                    height="12"
                    src="../../assets/icons/cross.svg"
                    alt="delete"
                    class="close"
                  />
                </button>
              </div>
            </template>
            <template #content>
              <ScrollBar>
                <div class="form-body-wrapper">
                  <InputField
                    v-model="reference"
                    label-text="Supplier Reference"
                    placeholder="Enter a reference"
                  />
                  <div class="w-full flex gap-3">
                    <InputField
                      v-model="fuelQuantity"
                      class="w-6/12"
                      label-text="Maximum Release Volume"
                      placeholder="Please enter quantity"
                    />
                    <SelectField
                      v-model="fuelUom"
                      class="w-6/12"
                      label-text="&nbsp;"
                      placeholder=""
                      label="description_plural"
                      :options="fuelQuantityUnits"
                      :errors="errors.fuelUom"
                    ></SelectField>
                  </div>
                  <div class="flex items-center justify-start pb-[1rem]">
                    <CheckboxField
                      v-model="captainsRequest"
                      :size="'20px'"
                      class="mb-0 mr-[0.25rem] ml-[0.1rem]"
                    />
                    <p class="text-base whitespace-nowrap font-semibold text-main">
                      Captain’s Request?
                    </p>
                  </div>
                  <div class="w-full flex gap-x-3 mb-[1rem]">
                    <div class="w-6/12 min-w-[132px]">
                      <Label
                        :required="false"
                        label-text="Release Valid From (UTC)"
                        class="whitespace-nowrap font-semibold"
                      />
                      <FlatPickr
                        ref="departureDateRef"
                        v-model="fromDate.date"
                        :config="flatpickerConfig"
                      />
                    </div>
                    <div class="flex flex-col w-6/12">
                      <Label :required="false" label-text="&nbsp;" class="whitespace-nowrap" />
                      <FlatPickr
                        v-model="fromDate.time"
                        placeholder="Time"
                        :config="flatpickerTimeConfig"
                        class="!pr-0"
                      />
                    </div>
                  </div>
                  <div class="w-full flex gap-x-3 mb-[1rem]">
                    <div class="w-6/12 min-w-[132px]">
                      <Label
                        :required="false"
                        label-text="Release Valid To (UTC)"
                        class="whitespace-nowrap font-semibold"
                      />
                      <FlatPickr
                        ref="departureDateRef"
                        v-model="toDate.date"
                        :config="flatpickerConfig"
                      />
                    </div>
                    <div class="flex flex-col w-6/12">
                      <Label :required="false" label-text="&nbsp;" class="whitespace-nowrap" />
                      <FlatPickr
                        v-model="toDate.time"
                        placeholder="Time"
                        :config="flatpickerTimeConfig"
                        class="!pr-0"
                      />
                    </div>
                  </div>
                  <div class="flex items-center justify-start mb-[0.75rem] gap-3">
                    <button class="modal-button icon" @click="onFileInputClick()">
                      <img
                        height="20"
                        width="20"
                        :src="
                          file
                            ? getImageUrl('assets/icons/file.svg')
                            : getImageUrl('assets/icons/paperclip.svg')
                        "
                        alt="attachment"
                      />
                    </button>
                    <input
                      ref="fileInputAddDocument"
                      class="hidden"
                      type="file"
                      @change="onChangeFile($event)"
                    />
                    <p class="text-base whitespace-nowrap font-semibold text-main">
                      {{
                        (file! as File)?.name
                          ? (file! as File)?.name.split('.')[0].substring(0, 40) +
                            '.' +
                            (file! as File)?.name.split('.')[1]
                          : ' Supplier Fuel Release'
                      }}
                    </p>
                  </div>
                </div>
              </ScrollBar>
            </template>
          </OrderForm>
        </div>
        <div class="order-modal-footer flex items-center">
          <Loading v-if="isSending" class="mr-4" />
          <button class="modal-button cancel" @click.stop="emit('modal-close')">Cancel</button>
          <button class="modal-button submit" @click.stop="onSubmit()">Confirm</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { type Ref, ref, shallowRef, watch } from 'vue';
import { computed } from 'vue';
import { useQueryClient } from '@tanstack/vue-query';
import { useOrderStore } from '@/stores/useOrderStore';
import OrderForm from '@/components/forms/OrderForm.vue';
import { useMutationConfirmSupplierOrderRequest } from '@/services/mutations/order';
import { useQueryUpliftFuelQuantityUnits } from '@/services/queries/uplift';
import { getImageUrl } from '@/helpers';
import { notify } from '@/helpers/toast';
import { flatpickerConfig, flatpickerTimeConfig } from '../FlatPickr/flatpicker.constants';
import FlatPickr from '../FlatPickr/FlatPickr.vue';
import CheckboxField from '../forms/fields/CheckboxField.vue';
import InputField from '../forms/fields/InputField.vue';
import SelectField from '../forms/fields/SelectField.vue';
import Label from '../forms/Label.vue';
import Loading from '../forms/Loading.vue';
import ScrollBar from '../forms/ScrollBar.vue';

import type { ITypeReference } from 'shared/types';

const props = defineProps({
  isOpen: Boolean
});

const emit = defineEmits(['modal-close', 'modal-submit']);
const target = ref(null);

const orderStore = useOrderStore();
const orderId = computed(() => orderStore.order?.id);
const fromDate = ref({
  date: '',
  time: ''
});
const toDate = ref({
  date: '',
  time: ''
});
const reference = shallowRef('');
const captainsRequest = shallowRef(false);
const fuelQuantity = shallowRef('');
const fuelUom: Ref<ITypeReference | null> = ref(null);
const file = ref(null);
const fileInputAddDocument = ref(null);
const enabled = ref(false);

const errors = ref({
  fuelQuantity: '',
  fuelUom: ''
});
const hasErrors = computed(() => Object.values(errors.value).some(Boolean));
const queryClient = useQueryClient();
const onChangeFile = (event: any) => {
  const fileData = event.target.files[0];
  if (fileData) {
    file.value = fileData;
  }
};

const onFileInputClick = () => {
  (fileInputAddDocument.value! as HTMLElement).click();
};

const { mutate: confirmOrderMutation, isPending: isSending } =
  useMutationConfirmSupplierOrderRequest();

const { data: fuelQuantityUnits } = useQueryUpliftFuelQuantityUnits({ enabled });

const refreshForm = () => {
  fromDate.value = {
    date: '',
    time: ''
  };
  toDate.value = {
    date: '',
    time: ''
  };
  reference.value = '';
  captainsRequest.value = false;
  fuelQuantity.value = '';
  fuelUom.value = null;
  file.value = null;
  fileInputAddDocument.value = null;
  errors.value = {
    fuelQuantity: '',
    fuelUom: ''
  };
};

const validate = () => {
  errors.value = {
    fuelUom:
      (fuelQuantity.value === '' && fuelUom.value === null) || (fuelQuantity.value && fuelUom.value)
        ? ''
        : 'Please select an uom',
    fuelQuantity:
      fuelQuantity.value === '' || parseInt(fuelQuantity.value) > 0
        ? ''
        : 'Please enter a quantity more than 0'
  };
};

const onSubmit = async () => {
  validate();
  if (hasErrors.value) {
    return notify('Error while submitting, please fill the required fields ', 'error');
  } else {
    const payload = {
      captains_request: captainsRequest.value
    };
    if (fuelUom.value) {
      (payload as any)['maximum_quantity_uom'] = fuelUom.value!.id;
    }
    if (file.value) {
      (payload as any)['file'] = file.value;
    }
    if (fromDate.value.date) {
      (payload as any)['valid_from'] = `${fromDate.value.date}${
        fromDate.value.time ? 'T' + fromDate.value.time + ':00.000Z' : ''
      }`;
    }
    if (toDate.value.date) {
      (payload as any)['valid_to'] = `${toDate.value.date}${
        toDate.value.time ? 'T' + toDate.value.time + ':00.000Z' : ''
      }`;
    }
    if (fuelQuantity.value) {
      (payload as any)['maximum_quantity_value'] = fuelQuantity.value;
    }
    if (reference.value) {
      (payload as any)['supplier_reference'] = reference.value;
    }

    await confirmOrderMutation(
      {
        orderId: orderId.value!,
        payload: payload
      },
      {
        onSuccess: () => {
          notify('Order confirmed successfully!', 'success');
          queryClient.invalidateQueries({ queryKey: ['orderStatus', orderId.value] });
          emit('modal-close');
          refreshForm();
        }
      }
    );
  }
};

watch(
  () => props.isOpen,
  (isOpen) => {
    enabled.value = isOpen;
  }
);
</script>

<style scoped lang="scss">
.confirm-supplier-modal {
  .modal-button {
    &.icon {
      background-color: rgba(240, 242, 252, 1);
      color: rgb(81 93 138);
      padding: 0.75rem;
      border-radius: 0.75rem;
      height: 100%;
    }
  }

  .ticket-error {
    font-size: 0.75rem;
    color: rgb(225, 29, 72);
  }
}
</style>
