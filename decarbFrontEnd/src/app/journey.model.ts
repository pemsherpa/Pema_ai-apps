export class Journey {
    constructor(
      public title: string,
      public scope: string[],
      public years: number,
      public months: number,
      public days: number,
      public costSavings: number,
      public costUnit: string,
      public co2Savings: number
    ) {}
  }
  