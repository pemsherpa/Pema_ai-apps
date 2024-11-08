// main.ts
import { bootstrapApplication } from '@angular/platform-browser';
import { appConfig } from './app/app.config';
import { AppComponent } from './app/app.component';
import { provideHttpClient, withFetch } from '@angular/common/http';

// Add provideHttpClient with `withFetch()` to the existing appConfig providers
const combinedConfig = {
  ...appConfig,
  providers: [
    ...appConfig.providers,
    provideHttpClient(withFetch()) // Enables fetch for better performance in SSR
  ],
};

bootstrapApplication(AppComponent, combinedConfig)
  .catch((err) => console.error(err));


