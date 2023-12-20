import { NgModule } from '@angular/core'
import { Routes } from '@angular/router'
import { NativeScriptRouterModule } from '@nativescript/angular'
import { WelcomePageComponent } from './welcome-page/welcome-page.component'


const routes: Routes = [
  { path: '', component: WelcomePageComponent },

]

@NgModule({
  imports: [NativeScriptRouterModule.forRoot(routes)],
  exports: [NativeScriptRouterModule],
})

export class AppRoutingModule {}
