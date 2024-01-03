import { Component, Input } from '@angular/core';
import { RouterExtensions } from '@nativescript/angular';
import { Page } from '@nativescript/core';
import { isAndroid } from "@nativescript/core";

declare var android: any;


@Component({
  selector: 'ns-action-bar',
  templateUrl: './action-bar.component.html',
  styleUrls: ['./action-bar.component.css']
})
export class ActionBarComponent {

  constructor(
    private page: Page,
    private router: RouterExtensions,
  ) {}

  @Input() title: string;
  @Input() showBackButton = true;
  @Input() hasHome = true;

  get canGoBack() {
    return this.router.canGoBack() && this.showBackButton;
  }

  onGoBack() {
    this.router.backToPreviousPage();
  }

  onLoadedActionBar() {
    if (isAndroid) {
      const androidToolbar = this.page.actionBar.nativeView;
      const backButton = androidToolbar.getNavigationIcon();
      let color = "#101010";
      if (backButton) {
        backButton.setColorFilter(
          android.graphics.Color.parseColor(color),
          <any>android.graphics.PorterDuff.Mode.SRC_ATOP
        );
      }
    }
  }

  onGoHome() {
    this.router.navigate(["/"], { clearHistory: true });
  }

}
