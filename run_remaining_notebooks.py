#!/usr/bin/env python3
"""
Run the remaining notebook experiments with GNN integration and comparison
"""

import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import networkx as nx
from pathlib import Path
import sys
import os
import time
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.metrics.pairwise import cosine_similarity

# Add current directory to path
sys.path.append('.')

def run_tissue_net_analysis():
    """Run tissue network analysis"""
    print("Running Tissue Network Analysis...")
    
    try:
        # Load data
        with pd.HDFStore('./data/gene_network_data.h5') as store:
            tec = store['TEC']
            rna = store['RNA']
        
        print(f"Loaded TEC data: {tec.shape}")
        print(f"Loaded RNA data: {rna.shape}")
        
        # Basic tissue network analysis
        np_tec = np.abs(tec.to_numpy())
        np_rna = np.abs(rna.to_numpy())
        
        # Calculate network properties at different thresholds
        thresholds = [0.9, 0.85, 0.8, 0.75, 0.7, 0.65, 0.6]
        results = {'threshold': [], 'tec_edges': [], 'rna_edges': [], 'tec_nodes': [], 'rna_nodes': []}
        
        for thresh in thresholds:
            # TEC network
            tec_adj = (np_tec > thresh).astype(int)
            np.fill_diagonal(tec_adj, 0)
            tec_G = nx.from_numpy_array(tec_adj)
            
            # RNA network  
            rna_adj = (np_rna > thresh).astype(int)
            np.fill_diagonal(rna_adj, 0)
            rna_G = nx.from_numpy_array(rna_adj)
            
            results['threshold'].append(thresh)
            results['tec_edges'].append(tec_G.number_of_edges())
            results['rna_edges'].append(rna_G.number_of_edges())
            results['tec_nodes'].append(len([n for n in tec_G.nodes() if tec_G.degree(n) > 0]))
            results['rna_nodes'].append(len([n for n in rna_G.nodes() if rna_G.degree(n) > 0]))
        
        # Create plot
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Edges comparison
        ax1.plot(results['threshold'], results['tec_edges'], 'o-', label='TEC', color='skyblue')
        ax1.plot(results['threshold'], results['rna_edges'], 's-', label='RNA', color='lightcoral')
        ax1.set_xlabel('Threshold')
        ax1.set_ylabel('Number of Edges')
        ax1.set_title('Network Edges vs Threshold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        ax1.set_yscale('log')
        
        # Nodes comparison
        ax2.plot(results['threshold'], results['tec_nodes'], 'o-', label='TEC', color='skyblue')
        ax2.plot(results['threshold'], results['rna_nodes'], 's-', label='RNA', color='lightcoral')
        ax2.set_xlabel('Threshold')
        ax2.set_ylabel('Connected Nodes')
        ax2.set_title('Connected Nodes vs Threshold')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('analysis_results/tissue_network_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("Tissue network analysis completed!")
        return results
        
    except Exception as e:
        print(f"Error in tissue network analysis: {e}")
        return None

def run_rna_comparison():
    """Run RNA comparison analysis"""
    print("Running RNA Comparison Analysis...")
    
    try:
        # Load data
        with pd.HDFStore('./data/gene_network_data.h5') as store:
            tec = store['TEC']
            rna = store['RNA']
        
        # Calculate correlation between TEC and RNA networks
        np_tec = np.abs(tec.to_numpy())
        np_rna = np.abs(rna.to_numpy())
        
        # Network comparison at threshold 0.75
        thresh = 0.75
        tec_adj = (np_tec > thresh).astype(int)
        rna_adj = (np_rna > thresh).astype(int)
        
        np.fill_diagonal(tec_adj, 0)
        np.fill_diagonal(rna_adj, 0)
        
        # Create networks
        tec_G = nx.from_numpy_array(tec_adj)
        rna_G = nx.from_numpy_array(rna_adj)
        
        # Calculate network properties
        tec_props = {
            'nodes': tec_G.number_of_nodes(),
            'edges': tec_G.number_of_edges(),
            'connected_components': nx.number_connected_components(tec_G),
            'avg_clustering': nx.average_clustering(tec_G),
            'density': nx.density(tec_G)
        }
        
        rna_props = {
            'nodes': rna_G.number_of_nodes(),
            'edges': rna_G.number_of_edges(),
            'connected_components': nx.number_connected_components(rna_G),
            'avg_clustering': nx.average_clustering(rna_G),
            'density': nx.density(rna_G)
        }
        
        # Create comparison plot
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
        
        # Network size comparison
        networks = ['TEC', 'RNA']
        edges = [tec_props['edges'], rna_props['edges']]
        components = [tec_props['connected_components'], rna_props['connected_components']]
        
        ax1.bar(networks, edges, color=['skyblue', 'lightcoral'], alpha=0.8)
        ax1.set_ylabel('Number of Edges')
        ax1.set_title('Network Size Comparison')
        ax1.grid(True, alpha=0.3)
        
        ax2.bar(networks, components, color=['skyblue', 'lightcoral'], alpha=0.8)
        ax2.set_ylabel('Connected Components')
        ax2.set_title('Network Fragmentation')
        ax2.grid(True, alpha=0.3)
        
        # Clustering and density
        clustering = [tec_props['avg_clustering'], rna_props['avg_clustering']]
        density = [tec_props['density'], rna_props['density']]
        
        ax3.bar(networks, clustering, color=['skyblue', 'lightcoral'], alpha=0.8)
        ax3.set_ylabel('Average Clustering')
        ax3.set_title('Network Clustering')
        ax3.grid(True, alpha=0.3)
        
        ax4.bar(networks, density, color=['skyblue', 'lightcoral'], alpha=0.8)
        ax4.set_ylabel('Network Density')
        ax4.set_title('Network Density')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('analysis_results/rna_comparison_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("RNA comparison analysis completed!")
        return {'tec': tec_props, 'rna': rna_props}
        
    except Exception as e:
        print(f"Error in RNA comparison: {e}")
        return None

def run_powerlaw_analysis():
    """Run power law analysis"""
    print("Running Power Law Analysis...")
    
    try:
        # Load data
        with pd.HDFStore('./data/gene_network_data.h5') as store:
            tec = store['TEC']
        
        np_tec = np.abs(tec.to_numpy())
        
        # Create network at threshold 0.75
        thresh = 0.75
        adj_matrix = (np_tec > thresh).astype(int)
        np.fill_diagonal(adj_matrix, 0)
        G = nx.from_numpy_array(adj_matrix)
        
        # Get degree sequence
        degrees = [G.degree(n) for n in G.nodes()]
        degree_counts = {}
        for d in degrees:
            degree_counts[d] = degree_counts.get(d, 0) + 1
        
        # Remove zero degrees
        degree_counts = {k: v for k, v in degree_counts.items() if k > 0}
        
        if len(degree_counts) > 1:
            degrees_list = list(degree_counts.keys())
            counts_list = list(degree_counts.values())
            
            # Calculate power law fit
            log_degrees = np.log(degrees_list)
            log_counts = np.log(counts_list)
            
            # Linear regression for power law
            coeffs = np.polyfit(log_degrees, log_counts, 1)
            alpha = -coeffs[0]  # Power law exponent
            
            # Create plot
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
            
            # Degree distribution
            ax1.scatter(degrees_list, counts_list, alpha=0.7, color='skyblue')
            ax1.set_xlabel('Degree')
            ax1.set_ylabel('Frequency')
            ax1.set_title('Degree Distribution')
            ax1.set_xscale('log')
            ax1.set_yscale('log')
            ax1.grid(True, alpha=0.3)
            
            # Power law fit
            fit_line = np.exp(coeffs[1]) * np.array(degrees_list) ** coeffs[0]
            ax1.plot(degrees_list, fit_line, 'r-', alpha=0.8, 
                    label=f'Power law fit (α={alpha:.2f})')
            ax1.legend()
            
            # Log-log plot
            ax2.scatter(log_degrees, log_counts, alpha=0.7, color='lightcoral')
            ax2.plot(log_degrees, np.polyval(coeffs, log_degrees), 'r-', alpha=0.8)
            ax2.set_xlabel('log(Degree)')
            ax2.set_ylabel('log(Frequency)')
            ax2.set_title(f'Power Law Fit (α={alpha:.2f})')
            ax2.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.savefig('analysis_results/powerlaw_analysis.png', dpi=300, bbox_inches='tight')
            plt.close()
            
            print(f"Power law analysis completed! Exponent α = {alpha:.3f}")
            return {'alpha': alpha, 'r_squared': np.corrcoef(log_degrees, log_counts)[0,1]**2}
        else:
            print("Insufficient data for power law analysis")
            return None
            
    except Exception as e:
        print(f"Error in power law analysis: {e}")
        return None

def run_supplemental_analysis():
    """Run supplemental figure analysis based on supp_fig1.ipynb"""
    print("Running Supplemental Analysis...")
    
    try:
        # Load data
        with pd.HDFStore('./data/gene_network_data.h5') as store:
            tec = store['TEC']
            rna = store['RNA']
        
        np_tec_abs = np.abs(tec.to_numpy(copy=True))
        np_rna_abs = np.abs(rna.to_numpy(copy=True))
        
        # Check same gene list between TEC and RNA
        genes_match = (tec.columns == rna.columns).all()
        print(f"Gene lists match: {genes_match}")
        
        # Analyze network properties at different thresholds
        thresholds = [0.9, 0.85, 0.8, 0.75, 0.7, 0.65, 0.6, 0.55, 0.5]
        
        tec_num_cc = []
        tec_isolated_nodes = []
        rna_num_cc = []
        rna_isolated_nodes = []
        
        tec_num_nodes = []
        tec_num_edges = []
        rna_num_nodes = []
        rna_num_edges = []
        
        for th in thresholds:
            # TEC network
            tec_adj = (np_tec_abs > th).astype(int)
            np.fill_diagonal(tec_adj, 0)
            tec_G = nx.from_numpy_array(tec_adj)
            
            # RNA network
            rna_adj = (np_rna_abs > th).astype(int)
            np.fill_diagonal(rna_adj, 0)
            rna_G = nx.from_numpy_array(rna_adj)
            
            # Connected components
            tec_cc = nx.number_connected_components(tec_G)
            rna_cc = nx.number_connected_components(rna_G)
            
            tec_num_cc.append(tec_cc)
            rna_num_cc.append(rna_cc)
            
            # Isolated nodes (degree 0)
            tec_isolated = len([n for n in tec_G.nodes() if tec_G.degree(n) == 0])
            rna_isolated = len([n for n in rna_G.nodes() if rna_G.degree(n) == 0])
            
            tec_isolated_nodes.append(tec_isolated)
            rna_isolated_nodes.append(rna_isolated)
            
            # Connected nodes and edges
            tec_connected = len([n for n in tec_G.nodes() if tec_G.degree(n) > 0])
            rna_connected = len([n for n in rna_G.nodes() if rna_G.degree(n) > 0])
            
            tec_num_nodes.append(tec_connected)
            rna_num_nodes.append(rna_connected)
            tec_num_edges.append(tec_G.number_of_edges())
            rna_num_edges.append(rna_G.number_of_edges())
        
        # Create supplemental figures
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Connected components comparison
        x = np.arange(len(thresholds))
        bar_width = 0.35
        
        ax1.bar(x - bar_width/2, tec_num_cc, width=bar_width, color='skyblue', label='TEC')
        ax1.bar(x + bar_width/2, rna_num_cc, width=bar_width, color='lightsalmon', label='RNA')
        ax1.set_xlabel('Threshold')
        ax1.set_ylabel('Number of Connected Components')
        ax1.set_title('Connected Components vs Threshold')
        ax1.set_xticks(x)
        ax1.set_xticklabels(thresholds)
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Nodes and edges comparison
        ymax = max(max(tec_num_edges), max(rna_num_edges))
        
        ax2.plot(x, tec_num_nodes, marker='s', markersize=7, label='TEC connected nodes', color='skyblue')
        ax2.plot(x, tec_num_edges, marker='<', markersize=7, label='TEC edges', color='skyblue')
        ax2.plot(x, rna_num_nodes, marker='s', markersize=7, label='RNA connected nodes', color='lightsalmon')
        ax2.plot(x, rna_num_edges, marker='<', markersize=7, label='RNA edges', color='lightsalmon')
        
        ax2.axhline(y=11088, linestyle='--', color='gray', alpha=0.7, label='Max nodes')
        ax2.axvline(x=3, linestyle='-.', color='darkgreen', alpha=0.7, label='Threshold 0.75')
        ax2.set_yscale('log')
        ax2.set_xlabel('Threshold Index')
        ax2.set_ylabel('Count')
        ax2.set_title('Network Size vs Threshold')
        ax2.set_xticks(x)
        ax2.set_xticklabels(thresholds)
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('analysis_results/supplemental_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # Degree distribution analysis for RNA at threshold 0.75
        rna_adj_75 = (np_rna_abs > 0.75).astype(int)
        np.fill_diagonal(rna_adj_75, 0)
        rna_G_75 = nx.from_numpy_array(rna_adj_75)
        
        degree_sequence = sorted([d for n, d in rna_G_75.degree()], reverse=True)
        max_degree = max(degree_sequence) if degree_sequence else 0
        
        # Plot degree distribution
        plt.figure(figsize=(8, 6))
        if max_degree > 0:
            plt.hist(degree_sequence, bins=range(0, max_degree + 2), 
                    color='lightsalmon', edgecolor='none', align='left')
            plt.yscale('log')
        plt.xlabel('Node Degree')
        plt.ylabel('Frequency')
        plt.title('RNA Network Degree Distribution (Threshold 0.75)')
        plt.grid(True, alpha=0.3)
        plt.savefig('analysis_results/degree_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        results = {
            'thresholds': thresholds,
            'tec_connected_components': tec_num_cc,
            'rna_connected_components': rna_num_cc,
            'tec_connected_nodes': tec_num_nodes,
            'rna_connected_nodes': rna_num_nodes,
            'tec_edges': tec_num_edges,
            'rna_edges': rna_num_edges,
            'max_degree_rna_75': max_degree,
            'genes_match': genes_match
        }
        
        print("Supplemental analysis completed!")
        return results
        
    except Exception as e:
        print(f"Error in supplemental analysis: {e}")
        return None

def run_gnn_comparison():
    """Run GNN vs Traditional comparison analysis"""
    print("Running GNN vs Traditional Network Comparison...")
    
    try:
        # Load existing results
        gnn_results = None
        traditional_results = None
        
        # Try to load GNN results
        if os.path.exists('gnn_only_results.json'):
            with open('gnn_only_results.json', 'r') as f:
                gnn_data = json.load(f)
                gnn_results = gnn_data['gnn_results']
        
        # Try to load comparison results
        if os.path.exists('gnn_vs_traditional_comparison.json'):
            with open('gnn_vs_traditional_comparison.json', 'r') as f:
                comparison_data = json.load(f)
                traditional_results = comparison_data['traditional_results']
                if not gnn_results:
                    gnn_results = comparison_data['gnn_results']
        
        if not gnn_results or not traditional_results:
            print("Missing GNN or traditional results - running basic comparison")
            return run_basic_gnn_comparison()
        
        # Create comprehensive comparison plots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        # Performance comparison
        methods = ['GNN', 'Traditional']
        training_times = [gnn_results['training_time'], traditional_results['processing_time']]
        silhouette_scores = [gnn_results['silhouette_score'], traditional_results['silhouette_score']]
        
        ax1.bar(methods, training_times, color=['lightblue', 'lightcoral'], alpha=0.8)
        ax1.set_ylabel('Time (seconds)')
        ax1.set_title('Processing Time Comparison')
        ax1.set_yscale('log')
        ax1.grid(True, alpha=0.3)
        
        ax2.bar(methods, silhouette_scores, color=['lightblue', 'lightcoral'], alpha=0.8)
        ax2.set_ylabel('Silhouette Score')
        ax2.set_title('Clustering Quality Comparison')
        ax2.grid(True, alpha=0.3)
        
        # Network structure comparison
        predictions = [gnn_results['high_confidence_predictions'], traditional_results['high_confidence_predictions']]
        similarities = [gnn_results['mean_similarity'], traditional_results['mean_similarity']]
        
        ax3.bar(methods, predictions, color=['lightblue', 'lightcoral'], alpha=0.8)
        ax3.set_ylabel('High Confidence Predictions')
        ax3.set_title('Link Prediction Capability')
        ax3.set_yscale('log')
        ax3.grid(True, alpha=0.3)
        
        ax4.bar(methods, similarities, color=['lightblue', 'lightcoral'], alpha=0.8)
        ax4.set_ylabel('Mean Similarity')
        ax4.set_title('Network Similarity Analysis')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('analysis_results/gnn_vs_traditional_comprehensive.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # Create summary comparison table
        comparison_summary = {
            'Method': ['GNN', 'Traditional'],
            'Processing_Time': [f"{gnn_results['training_time']:.1f}s", f"{traditional_results['processing_time']:.1f}s"],
            'Silhouette_Score': [f"{gnn_results['silhouette_score']:.4f}", f"{traditional_results['silhouette_score']:.4f}"],
            'Clusters_Components': [gnn_results['optimal_clusters'], traditional_results['num_components']],
            'High_Conf_Predictions': [gnn_results['high_confidence_predictions'], traditional_results['high_confidence_predictions']],
            'Mean_Similarity': [f"{gnn_results['mean_similarity']:.4f}", f"{traditional_results['mean_similarity']:.4f}"]
        }
        
        comparison_df = pd.DataFrame(comparison_summary)
        comparison_df.to_csv('analysis_results/gnn_traditional_comparison_table.csv', index=False)
        
        print("GNN vs Traditional comparison completed!")
        return {
            'gnn_results': gnn_results,
            'traditional_results': traditional_results,
            'comparison_summary': comparison_summary
        }
        
    except Exception as e:
        print(f"Error in GNN comparison: {e}")
        return None

def run_basic_gnn_comparison():
    """Run basic GNN comparison if detailed results not available"""
    print("Running basic GNN analysis...")
    
    try:
        # Load data
        with pd.HDFStore('./data/gene_network_data.h5') as store:
            tec = store['TEC']
        
        np_tec_abs = np.abs(tec.to_numpy())
        threshold = 0.75
        
        # Traditional network analysis
        start_time = time.time()
        adj_matrix = (np_tec_abs > threshold).astype(int)
        np.fill_diagonal(adj_matrix, 0)
        G = nx.from_numpy_array(adj_matrix)
        
        # Traditional clustering (using degree-based features)
        degrees = np.array([G.degree(n) for n in G.nodes()])
        clustering_coeffs = np.array([nx.clustering(G, n) for n in G.nodes()])
        features = np.column_stack([degrees, clustering_coeffs])
        
        # Remove zero-degree nodes for clustering
        non_zero_mask = degrees > 0
        if np.sum(non_zero_mask) > 1:
            features_filtered = features[non_zero_mask]
            
            # Find optimal clusters
            silhouette_scores = []
            for k in range(2, min(11, len(features_filtered))):
                if len(features_filtered) >= k:
                    kmeans = KMeans(n_clusters=k, random_state=42)
                    labels = kmeans.fit_predict(features_filtered)
                    score = silhouette_score(features_filtered, labels)
                    silhouette_scores.append((k, score))
            
            if silhouette_scores:
                optimal_k, best_score = max(silhouette_scores, key=lambda x: x[1])
            else:
                optimal_k, best_score = 2, 0.0
        else:
            optimal_k, best_score = 1, 0.0
        
        traditional_time = time.time() - start_time
        
        # Basic comparison results
        basic_results = {
            'traditional': {
                'processing_time': traditional_time,
                'optimal_clusters': optimal_k,
                'silhouette_score': best_score,
                'network_edges': G.number_of_edges(),
                'connected_nodes': len([n for n in G.nodes() if G.degree(n) > 0])
            },
            'network_properties': {
                'total_genes': len(tec),
                'threshold': threshold,
                'density': nx.density(G),
                'components': nx.number_connected_components(G)
            }
        }
        
        print(f"Basic analysis completed - Traditional: {traditional_time:.1f}s, Clusters: {optimal_k}")
        return basic_results
        
    except Exception as e:
        print(f"Error in basic GNN comparison: {e}")
        return None

def create_final_summary():
    """Create final experimental summary"""
    print("Creating final experimental summary...")
    
    try:
        # Load all available results
        results_files = {
            'gnn_only': 'gnn_only_results.json',
            'gnn_vs_traditional': 'gnn_vs_traditional_comparison.json',
            'remaining_experiments': 'analysis_results/remaining_experiments_results.json'
        }
        
        all_data = {}
        for key, filename in results_files.items():
            if os.path.exists(filename):
                with open(filename, 'r') as f:
                    all_data[key] = json.load(f)
        
        # Create summary figure
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # Method comparison if available
        if 'gnn_vs_traditional' in all_data:
            gnn_data = all_data['gnn_vs_traditional']['gnn_results']
            trad_data = all_data['gnn_vs_traditional']['traditional_results']
            
            methods = ['GNN', 'Traditional']
            times = [gnn_data['training_time'], trad_data['processing_time']]
            silhouettes = [gnn_data['silhouette_score'], trad_data['silhouette_score']]
            
            ax1.bar(methods, times, color=['skyblue', 'lightcoral'], alpha=0.8)
            ax1.set_ylabel('Processing Time (s)')
            ax1.set_title('GNN vs Traditional: Processing Time')
            ax1.set_yscale('log')
            ax1.grid(True, alpha=0.3)
            
            ax2.bar(methods, silhouettes, color=['skyblue', 'lightcoral'], alpha=0.8)
            ax2.set_ylabel('Silhouette Score')
            ax2.set_title('GNN vs Traditional: Clustering Quality')
            ax2.grid(True, alpha=0.3)
        
        # Network analysis results
        if 'remaining_experiments' in all_data and all_data['remaining_experiments']['tissue_network']:
            tissue_data = all_data['remaining_experiments']['tissue_network']
            thresholds = tissue_data['threshold']
            tec_edges = tissue_data['tec_edges']
            
            ax3.plot(thresholds, tec_edges, 'o-', color='skyblue', linewidth=2, markersize=6)
            ax3.set_xlabel('Threshold')
            ax3.set_ylabel('Number of Edges')
            ax3.set_title('TEC Network: Edges vs Threshold')
            ax3.set_yscale('log')
            ax3.grid(True, alpha=0.3)
        
        # Power law analysis if available
        if 'remaining_experiments' in all_data and all_data['remaining_experiments']['powerlaw_analysis']:
            powerlaw_data = all_data['remaining_experiments']['powerlaw_analysis']
            alpha = powerlaw_data['alpha']
            r_squared = powerlaw_data['r_squared']
            
            ax4.text(0.5, 0.7, f'Power Law Exponent\nα = {alpha:.3f}', 
                    transform=ax4.transAxes, fontsize=14, ha='center',
                    bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
            ax4.text(0.5, 0.3, f'R² = {r_squared:.3f}', 
                    transform=ax4.transAxes, fontsize=12, ha='center',
                    bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.8))
            ax4.set_title('Power Law Analysis Results')
            ax4.set_xlim(0, 1)
            ax4.set_ylim(0, 1)
            ax4.axis('off')
        
        plt.tight_layout()
        plt.savefig('analysis_results/final_experimental_summary.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("Final experimental summary created!")
        return all_data
        
    except Exception as e:
        print(f"Error creating final summary: {e}")
        return None

def main():
    """Run all remaining notebook experiments with GNN integration"""
    print("Running Comprehensive Network Analysis Experiments")
    print("=" * 60)
    
    # Create results directory
    Path("analysis_results").mkdir(exist_ok=True)
    
    # Run traditional experiments
    print("\n1. Running Traditional Network Experiments...")
    tissue_results = run_tissue_net_analysis()
    rna_results = run_rna_comparison()
    powerlaw_results = run_powerlaw_analysis()
    supplemental_results = run_supplemental_analysis()
    
    # Run GNN comparison
    print("\n2. Running GNN vs Traditional Comparison...")
    gnn_comparison_results = run_gnn_comparison()
    
    # Create final summary
    print("\n3. Creating Final Summary...")
    final_summary = create_final_summary()
    
    # Save all results
    all_results = {
        'tissue_network': tissue_results,
        'rna_comparison': rna_results, 
        'powerlaw_analysis': powerlaw_results,
        'supplemental_analysis': supplemental_results,
        'gnn_comparison': gnn_comparison_results,
        'final_summary': 'Created successfully' if final_summary else 'Failed'
    }
    
    with open('analysis_results/comprehensive_experiments_results.json', 'w') as f:
        json.dump(all_results, f, indent=2, default=str)
    
    print("\n" + "=" * 60)
    print("ALL COMPREHENSIVE EXPERIMENTS COMPLETED!")
    print("=" * 60)
    print("Results saved to analysis_results/")
    print("- tissue_network_analysis.png")
    print("- rna_comparison_analysis.png") 
    print("- powerlaw_analysis.png")
    print("- supplemental_analysis.png")
    print("- degree_distribution.png")
    print("- gnn_vs_traditional_comprehensive.png")
    print("- gnn_traditional_comparison_table.csv")
    print("- final_experimental_summary.png")
    print("- comprehensive_experiments_results.json")
    
    # Print key findings
    if gnn_comparison_results and 'gnn_results' in gnn_comparison_results:
        gnn_data = gnn_comparison_results['gnn_results']
        trad_data = gnn_comparison_results['traditional_results']
        
        print("\nKEY FINDINGS:")
        print(f"- GNN Training Time: {gnn_data['training_time']:.1f}s")
        print(f"- Traditional Processing: {trad_data['processing_time']:.1f}s")
        print(f"- GNN Silhouette Score: {gnn_data['silhouette_score']:.4f}")
        print(f"- Traditional Silhouette: {trad_data['silhouette_score']:.4f}")
        print(f"- GNN Predictions: {gnn_data['high_confidence_predictions']:,}")
        print(f"- Traditional Predictions: {trad_data['high_confidence_predictions']:,}")
    
    if powerlaw_results:
        print(f"- Power Law Exponent: α = {powerlaw_results['alpha']:.3f}")

if __name__ == "__main__":
    main()