import { Component } from '@angular/core';
import { Dialogs } from '@nativescript/core';


@Component({
  selector: 'ns-bottom-bar',
  templateUrl: './bottom-bar.component.html',
  styleUrls: ['./bottom-bar.component.css']
})
export class BottomBarComponent {

  showInfo() {
    Dialogs.alert({
      title: 'Sigma Industry Evoluation',
      message: 'Welcome to image recognition powered by SIE-AI',
      okButtonText: 'Close',
      cancelable: true,
    })
  }
  
}
