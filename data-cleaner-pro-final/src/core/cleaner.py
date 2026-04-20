"""
Data Cleaner Pro - Core Module
Author: Igor.Lana | Igor.L.Z
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import json

class DataCleaner:
    """Sistema profissional de limpeza de dados"""
    
    def __init__(self, file_path: str, config: dict = None):
        self.file_path = Path(file_path)
        self.config = config or self._default_config()
        self.data = None
        self.original_stats = {}
        self.treated_stats = {}
        self.actions_log = []
        self.file_type = self.file_path.suffix.lower()
        
        if not self.file_path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
    
    def _default_config(self) -> dict:
        return {
            'remove_duplicates': True,
            'treat_nulls': True,
            'treat_outliers': True,
            'standardize_dates': True,
            'method_nulls': 'Mediana',
            'method_outliers': 'IQR',
            'output_format': 'Mesmo formato original'
        }
    
    def load_data(self):
        """Carrega dados do arquivo"""
        print(f"📂 Carregando: {self.file_path.name}")
        
        if self.file_type == '.csv':
            self.data = pd.read_csv(self.file_path)
        elif self.file_type in ['.xlsx', '.xls']:
            self.data = pd.read_excel(self.file_path)
        elif self.file_type == '.json':
            self.data = pd.read_json(self.file_path)
        else:
            raise ValueError(f"Formato {self.file_type} não suportado")
        
        print(f"✅ {len(self.data)} linhas, {len(self.data.columns)} colunas")
        return self
    
    def analyze(self):
        """Analisa estado atual dos dados"""
        self.original_stats = {
            'linhas': len(self.data),
            'colunas': len(self.data.columns),
            'valores_nulos': int(self.data.isnull().sum().sum()),
            'duplicatas': int(self.data.duplicated().sum()),
            'memoria_mb': float(self.data.memory_usage(deep=True).sum() / 1024**2)
        }
        return self.original_stats
    
    def clean(self):
        """Executa limpeza dos dados"""
        print("\n🔧 Iniciando limpeza...")
        
        # Remover duplicatas
        if self.config.get('remove_duplicates', True):
            before = len(self.data)
            self.data = self.data.drop_duplicates()
            removed = before - len(self.data)
            if removed > 0:
                self.actions_log.append(f"Removidas {removed} linhas duplicadas")
                print(f"  • Removidas {removed} duplicatas")
        
        # Tratar nulos
        if self.config.get('treat_nulls', True):
            nulls_before = self.data.isnull().sum().sum()
            for col in self.data.columns:
                if self.data[col].dtype in ['int64', 'float64']:
                    self.data[col] = self.data[col].fillna(self.data[col].median())
                else:
                    self.data[col] = self.data[col].fillna("desconhecido")
            nulls_after = self.data.isnull().sum().sum()
            treated = nulls_before - nulls_after
            if treated > 0:
                self.actions_log.append(f"Tratados {treated} valores nulos")
                print(f"  • Tratados {treated} nulos")
        
        # Tratar outliers
        if self.config.get('treat_outliers', True):
            outliers_count = 0
            for col in self.data.select_dtypes(include=[np.number]).columns:
                Q1 = self.data[col].quantile(0.25)
                Q3 = self.data[col].quantile(0.75)
                IQR = Q3 - Q1
                if IQR > 0:
                    lower = Q1 - 1.5 * IQR
                    upper = Q3 + 1.5 * IQR
                    outliers = ((self.data[col] < lower) | (self.data[col] > upper)).sum()
                    if outliers > 0:
                        self.data[col] = self.data[col].clip(lower, upper)
                        outliers_count += outliers
            if outliers_count > 0:
                self.actions_log.append(f"Tratados {outliers_count} outliers")
                print(f"  • Tratados {outliers_count} outliers")
        
        # Padronizar datas
        if self.config.get('standardize_dates', True):
            dates_found = 0
            for col in self.data.columns:
                if self.data[col].dtype == 'object':
                    try:
                        self.data[col] = pd.to_datetime(self.data[col], errors='coerce')
                        dates_found += 1
                    except:
                        pass
            if dates_found > 0:
                self.actions_log.append(f"Padronizadas {dates_found} colunas de data")
                print(f"  • Padronizadas {dates_found} datas")
        
        return self
    
    def generate_report(self) -> dict:
        """Gera relatório completo"""
        self.treated_stats = {
            'linhas': len(self.data),
            'colunas': len(self.data.columns),
            'valores_nulos': int(self.data.isnull().sum().sum()),
            'duplicatas': int(self.data.duplicated().sum()),
            'memoria_mb': float(self.data.memory_usage(deep=True).sum() / 1024**2)
        }
        
        report = {
            'arquivo': self.file_path.name,
            'data_processamento': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'assinatura': 'Igor.Lana - Dados limpos, decisões claras',
            'configuracoes': self.config,
            'acoes_realizadas': self.actions_log,
            'estatisticas_antes': self.original_stats,
            'estatisticas_depois': self.treated_stats,
            'melhorias': {
                'reducao_linhas': self.original_stats['linhas'] - self.treated_stats['linhas'],
                'reducao_nulos': self.original_stats['valores_nulos'] - self.treated_stats['valores_nulos'],
                'reducao_duplicatas': self.original_stats['duplicatas'] - self.treated_stats['duplicatas']
            },
            'recomendacoes': ["✅ Dados em excelente estado para análise"]
        }
        
        # Salvar relatório
        report_dir = Path('reports')
        report_dir.mkdir(exist_ok=True)
        report_file = report_dir / f"{self.file_path.stem}_relatorio.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return report
    
    def save(self) -> Path:
        """Salva dados tratados"""
        output_dir = Path('output')
        output_dir.mkdir(exist_ok=True)
        
        output_file = output_dir / f"{self.file_path.stem}_tratado{self.file_type}"
        
        if self.file_type == '.csv':
            self.data.to_csv(output_file, index=False, encoding='utf-8')
        elif self.file_type in ['.xlsx', '.xls']:
            self.data.to_excel(output_file, index=False)
        elif self.file_type == '.json':
            self.data.to_json(output_file, orient='records', indent=2, force_ascii=False)
        
        print(f"\n💾 Arquivo salvo: {output_file}")
        return output_file
    
    def run(self) -> dict:
        """Executa pipeline completo"""
        self.load_data()
        self.analyze()
        self.clean()
        report = self.generate_report()
        self.save()
        
        print("\n" + "="*50)
        print("📊 RESUMO DO TRATAMENTO")
        print("="*50)
        print(f"Linhas: {self.original_stats['linhas']} → {self.treated_stats['linhas']}")
        print(f"Nulos: {self.original_stats['valores_nulos']} → {self.treated_stats['valores_nulos']}")
        print(f"Duplicatas: {self.original_stats['duplicatas']} → {self.treated_stats['duplicatas']}")
        print("="*50)
        print("✅ Tratamento concluído com sucesso!")
        
        return report
