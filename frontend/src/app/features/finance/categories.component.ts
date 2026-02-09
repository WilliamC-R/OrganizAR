import { Component, OnInit } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';

import { FinanceService, Category } from './finance.service';

@Component({
  selector: 'app-categories',
  templateUrl: './categories.component.html'
})
export class CategoriesComponent implements OnInit {
  categories: Category[] = [];

  form = this.fb.group({
    name: ['', Validators.required],
    kind: ['expense', Validators.required]
  });

  constructor(private finance: FinanceService, private fb: FormBuilder) {}

  ngOnInit(): void {
    this.loadCategories();
  }

  loadCategories(): void {
    this.finance.listCategories().subscribe((response) => (this.categories = response.categories));
  }

  submit(): void {
    if (this.form.invalid) {
      return;
    }
    this.finance.createCategory(this.form.getRawValue()).subscribe(() => {
      this.form.reset({ kind: 'expense' });
      this.loadCategories();
    });
  }
}
