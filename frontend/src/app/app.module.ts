import { NgModule, NO_ERRORS_SCHEMA } from "@angular/core";
import { NativeScriptModule } from "@nativescript/angular";
import { SharedModule } from "./shared/shared.module";

import { AppRoutingModule } from "./app-routing.module";
import { AppComponent } from "./app.component";
import { WelcomePageComponent } from "./welcome-page/welcome-page.component";
import { ImageCaptureComponent } from './image-capture/image-capture.component';

@NgModule({
  bootstrap: [AppComponent],
  imports: [NativeScriptModule, AppRoutingModule, SharedModule],
  declarations: [
    AppComponent,
    WelcomePageComponent,
    ImageCaptureComponent,
  ],
  providers: [],
  schemas: [NO_ERRORS_SCHEMA],
})
export class AppModule {}
