import { NgModule, NO_ERRORS_SCHEMA, APP_INITIALIZER } from "@angular/core";
import {
  NativeScriptModule,
  NativeScriptFormsModule
} from "@nativescript/angular";

import { AppComponent } from "./app.component";
import { AppRoutingModule } from "./app-routing.module";
import { SharedModule } from "./shared/shared.module";
import { ReactiveFormsModule } from "@angular/forms";
import { WelcomePageComponent } from "./welcome-page/welcome-page.component";
import { NativeScriptHttpClientModule } from "@klippa/nativescript-http/angular";

import { SessionService } from "~/app/shared/auth/session.service";
import { ImageCaptureComponent } from "./image-capture/image-capture.component";
import { PredictionComponent } from './prediction/prediction.component';
// Uncomment and add to NgModule imports if you need to use two-way binding
// import { NativeScriptFormsModule } from '@nativescript/angular/forms';


export function sessionServiceInit(sessionService: SessionService) {
  return () => sessionService.authenticate();
}

@NgModule({
  bootstrap: [AppComponent],
  imports: [
    NativeScriptModule,
    NativeScriptFormsModule,
    AppRoutingModule,
    ReactiveFormsModule,
    SharedModule,
    NativeScriptHttpClientModule
  ],
  declarations: [
    AppComponent,
    WelcomePageComponent,
    ImageCaptureComponent,
    PredictionComponent
   
  ],
  providers: [
    SessionService,
    {
      provide: APP_INITIALIZER,
      multi: true,
      useFactory: sessionServiceInit,
      deps: [SessionService],
    },
  ],
  schemas: [NO_ERRORS_SCHEMA],
})
/*
Pass your application module to the bootstrapModule function located in main.ts to start your app
*/
export class AppModule {}
