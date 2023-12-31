import { NO_ERRORS_SCHEMA, NgModule } from "@angular/core";
import { NativeScriptFormsModule } from "@nativescript/angular";
import { ActionBarComponent } from "./ui/action-bar/action-bar.component";
import {
  NativeScriptCommonModule,
  NativeScriptRouterModule,
} from "@nativescript/angular";
import { BottomBarComponent } from "./ui/bottom-bar/bottom-bar.component";
import { TakePictureButtonComponent } from "./buttons/take-picture-button/take-picture-button.component";

@NgModule({
  imports: [
    NativeScriptCommonModule,
    NativeScriptRouterModule,
    NativeScriptFormsModule,
  ],
  declarations: [
    ActionBarComponent,
    BottomBarComponent,
    TakePictureButtonComponent,
  ],
  exports: [ActionBarComponent, BottomBarComponent, TakePictureButtonComponent],
  schemas: [NO_ERRORS_SCHEMA],
})
export class SharedModule {}
