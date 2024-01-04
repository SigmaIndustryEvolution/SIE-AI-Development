import {
  Component,
  OnInit,
  AfterViewInit,
  ChangeDetectorRef,
  ViewContainerRef,
} from "@angular/core";
import { UIService } from "./shared/ui/ui.service";

@Component({
  selector: "ns-app",
  templateUrl: "./app.component.html",
})
export class AppComponent implements OnInit, AfterViewInit {
  activeChallenge = "";

  constructor(
    private uiService: UIService,
    private changeDetectionRef: ChangeDetectorRef,
    private vcRef: ViewContainerRef
  ) {
  }

  ngAfterViewInit() {
    this.changeDetectionRef.detectChanges();
  }

  ngOnInit() {
    this.uiService.setRootVCRef(this.vcRef);
  }

}
