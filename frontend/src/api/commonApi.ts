import axiosInstance from './axiosInstance';
import type { ApiResponse } from '@/types';

export interface CurrencyOption {
  code: string;
  name: string;
  symbol: string;
}

export interface ChoiceOption {
  value: string;
  label: string;
}

export interface CommonChoicesResponse {
  PartyType?: ChoiceOption[];
  BaseAssetType?: ChoiceOption[];
  CollateralAssetType?: ChoiceOption[];
  AssetCondition?: ChoiceOption[];
  IdentificationType?: ChoiceOption[];
}

export const commonApi = {
  getCurrencies: async (): Promise<CurrencyOption[]> => {
    const { data } = await axiosInstance.get<ApiResponse<CurrencyOption[]>>(
      '/common/currencies/',
    );
    return data.data ?? (data as unknown as CurrencyOption[]);
  },

  getChoices: async (): Promise<CommonChoicesResponse> => {
    const { data } =
      await axiosInstance.get<CommonChoicesResponse>('/common/choices/');
    return data;
  },
};
