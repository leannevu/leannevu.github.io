from flask import Blueprint, jsonify, render_template

from projects.services.optimization_service import Optimize

optimization_bp = Blueprint("optimization", __name__)


@optimization_bp.route('')
def optimization():
    return render_template('optimization/index.html')


@optimization_bp.route('/api/random-portfolio')
def get_random_portfolio():
    try:
        op_object = Optimize()

        results_as_object = op_object.optimize_portfolio()
        image = results_as_object.get('encoded_image')
        allocs = results_as_object.get('allocs')
        computations = results_as_object.get('computations')
        symbols = results_as_object.get('symbols')

        return jsonify({
            'image': image,
            'allocs': allocs,
            'computations': computations,
            'symbols': symbols,
        })

    except Exception as e:
        return jsonify({'error': str(e)})
