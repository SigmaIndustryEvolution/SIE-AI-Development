import { Component } from '@angular/core';
import { RouterExtensions } from '@nativescript/angular';

@Component({
  selector: 'ns-welcome-page',
  templateUrl: './welcome-page.component.html',
  styleUrls: ['./welcome-page.component.css']
})
export class WelcomePageComponent {

  constructor(private router: RouterExtensions) {}

  nextPage() {
    this.router.navigate(["/image-capture"]);
  }
  
}
