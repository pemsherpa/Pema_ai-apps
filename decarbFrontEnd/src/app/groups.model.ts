export interface MemberList {
    id: number;
    method: string;
    locations: string;
    frequency: number;
    cost_per_km: number;
    coords: [number, number];
    distance: number;
    emission: number;
    distane_from_firm: number;
    cost: number;
    carpool_group: number
}
export interface CommuteRec {
    group: number;
    members: MemberList[];
    message: string | null;
    money_savings: number;
    emission_savings: number;
    distance_saving: number;

}
export interface Groups {
  description: string;
  difficulty: number;
  cost_savings: number;
  co2_savings: number;
  total_cost: number;
  total_emissions: number;
  transition_percentage: number;
  commute_rec: CommuteRec[];
}