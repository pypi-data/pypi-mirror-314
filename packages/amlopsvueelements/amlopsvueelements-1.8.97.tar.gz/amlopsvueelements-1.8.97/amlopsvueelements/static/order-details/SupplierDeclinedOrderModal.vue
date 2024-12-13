<template>
  <div v-if="props.isOpen" class="order-modal">
    <div class="order-modal-wrapper">
      <div ref="target" class="order-modal-container">
        <div class="order-modal-body">
          <OrderForm add-default-classes is-modal>
            <template #header>
              <div class="header w-full flex justify-between">
                <div class="text-[1.25rem] font-medium text-grey-1000">Supplier Declined Order</div>
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
              <div class="form-body-wrapper">
                <Label label-text="Supplier" :required="false" />
                <p class="supplier mb-[24px]">{{ supplierName }}</p>
                <TextareaField
                  v-model="body"
                  class="w-full"
                  label-text="Reason Given for Decline"
                  placeholder="Reason"
                  :errors="bodyError"
                />
                <div class="counter flex w-full justify-end">
                  {{ `${body.length} / ${MAX_COMMENT_LENGTH}` }}
                </div>
              </div>
            </template>
          </OrderForm>
        </div>
        <div class="order-modal-footer">
          <Loading v-if="isDeclining" class="mr-4" />
          <button class="modal-button cancel" @click.stop="emit('modal-close')">Cancel</button>
          <button
            class="modal-button submit"
            :disabled="body.length > MAX_COMMENT_LENGTH || isDeclining"
            @click.stop="onSubmit"
          >
            Confirm
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { computed, ref } from 'vue';
import { useQueryClient } from '@tanstack/vue-query';
import { storeToRefs } from 'pinia';
import { useOrderReferenceStore } from '@/stores/useOrderReferenceStore';
import { useOrderStore } from '@/stores/useOrderStore';
import OrderForm from '@/components/forms/OrderForm.vue';
import { useMutationSupplierDeclinedOrder } from '@/services/mutations/order';
import { notify } from '@/helpers/toast';
import TextareaField from '../forms/fields/TextareaField.vue';
import Label from '../forms/Label.vue';
import Loading from '../forms/Loading.vue';

const props = defineProps({
  isOpen: Boolean
});

const emit = defineEmits(['modal-close', 'modal-submit']);

const MAX_COMMENT_LENGTH = 250;

const queryClient = useQueryClient();
const orderStore = useOrderStore();
const orderReferenceStore = useOrderReferenceStore();

const { supplyFuel, selectedSupplierInfo } = storeToRefs(orderReferenceStore);

const body = ref('');

const pricingCalculationRecord = computed(() => orderStore.order?.pricing_calculation_record);

const bodyError = computed(() =>
  body.value.length > MAX_COMMENT_LENGTH ? 'Reason is too long' : ''
);
const orderId = computed(() => orderStore.orderId);
const supplierName = computed(() => {
  const supplierKey = String(selectedSupplierInfo.value?.detailsId);

  return (
    supplyFuel.value?.results?.find((supplier) => supplier.key === supplierKey)?.supplier
      ?.full_repr ?? ''
  );
});

const { mutate: declineMutation, isPending: isDeclining } = useMutationSupplierDeclinedOrder();

const onSubmit = async () => {
  if (bodyError.value) {
    return notify('Error while submitting, form is not valid!', 'error');
  } else {
    await declineMutation(
      {
        orderId: orderId.value,
        payload: {
          decline_reason: body.value
        }
      },
      {
        onSuccess: () => {
          queryClient.invalidateQueries({ queryKey: ['orderStatus', orderId.value] });
          orderStore.changeStep(1);
          orderReferenceStore.fetchSupplierFuel(pricingCalculationRecord.value);
          emit('modal-close');
          emit('modal-submit');
        }
      }
    );
  }
};
</script>

<style scoped lang="scss">
.order-modal-footer {
  align-items: center;
  flex: 0 0 72px;
  min-height: 72px;

  .modal-button {
    max-height: 44px;
  }
}

.supplier {
  font-size: 16px;
  font-weight: 400;
  color: theme('colors.base.900');
  line-height: 24px;
}
</style>
