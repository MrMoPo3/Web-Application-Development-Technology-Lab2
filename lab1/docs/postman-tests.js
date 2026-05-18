const baseUrl = pm.collectionVariables.get('base_url') || 'http://127.0.0.1:8000';

pm.test('Server returned a successful response', function () {
  pm.expect(pm.response.code).to.be.oneOf([200, 201, 204]);
});

if (pm.info.requestName === 'Register User' || pm.info.requestName === 'Login User') {
  const body = pm.response.json();

  pm.test('Authentication token is returned', function () {
    pm.expect(body.token).to.be.a('string').and.not.empty;
  });

  pm.collectionVariables.set('token', body.token);
}

if (pm.info.requestName === 'Create Poll') {
  const body = pm.response.json();

  pm.test('Poll and choices are created', function () {
    pm.expect(body.id).to.exist;
    pm.expect(body.choices).to.be.an('array').with.length.greaterThan(1);
  });

  pm.collectionVariables.set('poll_id', body.id);
  pm.collectionVariables.set('choice_id', body.choices[0].id);
}

if (pm.info.requestName === 'Poll Stats') {
  const body = pm.response.json();

  pm.test('Poll statistics contain total votes', function () {
    pm.expect(body).to.have.property('total_votes');
    pm.expect(body.choices).to.be.an('array');
  });
}

if (pm.info.requestName === 'Online Users') {
  pm.test('Online users response is an array', function () {
    pm.expect(pm.response.json()).to.be.an('array');
  });
}
