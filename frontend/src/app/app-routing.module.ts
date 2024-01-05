import { NgModule } from '@angular/core'
import { Routes } from '@angular/router'
import { NativeScriptRouterModule } from '@nativescript/angular'
import { WelcomePageComponent } from './welcome-page/welcome-page.component'
import { ImageCaptureComponent } from './image-capture/image-capture.component'
import { PredictionComponent } from "./prediction/prediction.component";


const routes: Routes = [
  { path: '', component: WelcomePageComponent },
  { path: "image-capture", component: ImageCaptureComponent},
  { path: "prediction", component: PredictionComponent },


]

@NgModule({
  imports: [NativeScriptRouterModule.forRoot(routes)],
  exports: [NativeScriptRouterModule],
})

export class AppRoutingModule {}
