import { Component, OnInit } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';

import { FinanceService, Entry } from './finance.service';

@Component({
  selector: 'app-entries',
  templateUrl: './entries.component.html'
})
export class EntriesComponent implements OnInit {
  entries: Entry[] = [];

  form = this.fb.group({
    kind: ['expense', Validators.required],
    amount: ['', Validators.required],
    date: ['', Validators.required],
    category_id: ['', Validators.required],
    description: ['']
  });

  constructor(private finance: FinanceService, private fb: FormBuilder) {}

  ngOnInit(): void {
    this.loadEntries();
  }

  loadEntries(): void {
    this.finance.listEntries().subscribe((response) => (this.entries = response.entries));
  }

  submit(): void {
    if (this.form.invalid) {
      return;
    }
    this.finance.createEntry(this.form.getRawValue()).subscribe(() => {
      this.form.reset({ kind: 'expense' });
      this.loadEntries();
    });
  }
}
