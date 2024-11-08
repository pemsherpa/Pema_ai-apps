export interface ActionObject {
  name: string;
  description: string;
  date: string;
  percentageComplete: number;
}

export interface Company {
  name: string;
  revenue: number;
  savings: number;
  current_emissions: number;
  emissions_avoided: number;
  industry_type: string;
  industry_sector: string;
  description: string;
  lat: number;
  lng: number;
  logo: string;
  actions: ActionObject[];
}
